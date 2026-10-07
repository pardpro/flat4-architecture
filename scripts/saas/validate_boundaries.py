#!/usr/bin/env python3
"""F4A Architecture Boundary Validator for SaaS Profile.

Validates project architectural boundaries against declarative rules specified
in an f4a-boundaries.toml configuration file.
"""

import argparse
import ast
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:
        tomllib = None  # Handled at parse_config time


DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
}


@dataclass
class Finding:
    status: str  # "violation" | "unresolved"
    severity: str  # "error" | "warning"
    rule_name: str
    file_path: str
    line: int
    message: str
    imported: str | None = None


@dataclass
class Rule:
    name: str
    from_path: Path
    deny_modules: list[str]
    deny_paths: list[Path]
    severity: str
    message: str


def _parse_simple_toml(content: str) -> dict[str, Any]:
    """Minimal zero-dependency TOML subset parser for Python < 3.11 environments."""
    data: dict[str, Any] = {"project": {}, "rules": []}
    current_section = None
    current_rule: dict[str, Any] | None = None

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line == "[[rules]]":
            current_section = "rules"
            current_rule = {}
            data["rules"].append(current_rule)
            continue
        elif line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            continue

        if "=" in line:
            key, val = (part.strip() for part in line.split("=", 1))
            # Parse simple string, list of strings, or int
            parsed_val: Any
            if val.startswith('"') and val.endswith('"'):
                parsed_val = val[1:-1]
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                if not inner:
                    parsed_val = []
                else:
                    parsed_val = [
                        item.strip().strip('"').strip("'")
                        for item in inner.split(",")
                        if item.strip()
                    ]
            elif val.isdigit():
                parsed_val = int(val)
            else:
                parsed_val = val

            if current_section == "rules" and current_rule is not None:
                current_rule[key] = parsed_val
            elif current_section == "project":
                data["project"][key] = parsed_val
            elif current_section is None:
                data[key] = parsed_val

    return data


def parse_config(config_path: Path) -> tuple[Path, list[Rule]]:
    """Parse and validate the f4a-boundaries.toml file."""
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    if tomllib is not None:
        with config_path.open("rb") as f:
            data = tomllib.load(f)
    else:
        with config_path.open("r", encoding="utf-8") as f:
            data = _parse_simple_toml(f.read())

    project_cfg = data.get("project", {})
    root_str = project_cfg.get("root", ".")
    project_root = (config_path.parent / root_str).resolve()

    if not project_root.exists():
        raise FileNotFoundError(f"Configured project root does not exist: {project_root}")

    rules_data = data.get("rules", [])
    rules: list[Rule] = []

    for idx, r in enumerate(rules_data):
        name = r.get("name", f"rule-{idx + 1}")
        from_subpath = r.get("from")
        if not from_subpath:
            raise ValueError(f"Rule '{name}' is missing required 'from' field.")

        rule_from_path = (project_root / from_subpath).resolve()

        deny_modules = [m.strip() for m in r.get("deny_modules", []) if m.strip()]
        deny_paths_raw = r.get("deny_paths", [])
        deny_paths = [(project_root / p.strip()).resolve() for p in deny_paths_raw if p.strip()]

        severity = r.get("severity", "error").lower()
        if severity not in ("error", "warning"):
            severity = "error"

        msg = r.get("message", f"Import violates boundary rule '{name}'.")

        rules.append(
            Rule(
                name=name,
                from_path=rule_from_path,
                deny_modules=deny_modules,
                deny_paths=deny_paths,
                severity=severity,
                message=msg,
            )
        )

    return project_root, rules


class ImportExtractor(ast.NodeVisitor):
    """AST visitor to discover statically identifiable imports and dynamic calls."""

    def __init__(self, current_file: Path, project_root: Path):
        self.current_file = current_file
        self.project_root = project_root
        # Entries: (type, target_str_or_none, line_number)
        # type can be: 'module', 'relative_resolved_path', 'unresolved'
        self.discovered: list[tuple[str, Any, int]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.discovered.append(("module", alias.name, node.lineno))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level and node.level > 0:
            # Relative import: compute base dir relative to project_root
            current_dir = self.current_file.parent
            base_dir = current_dir
            for _ in range(node.level - 1):
                base_dir = base_dir.parent

            # Candidate file or package
            sub = node.module.replace(".", "/") if node.module else ""
            candidate = (base_dir / sub).resolve()
            self.discovered.append(("relative_resolved_path", candidate, node.lineno))
        elif node.module:
            self.discovered.append(("module", node.module, node.lineno))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        is_import_call = False
        # Check __import__("...")
        if isinstance(node.func, ast.Name) and node.func.id == "__import__" or (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "import_module"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "importlib"
        ):
            is_import_call = True

        if is_import_call:
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                self.discovered.append(("module", node.args[0].value, node.lineno))
            else:
                self.discovered.append(("unresolved", None, node.lineno))

        self.generic_visit(node)


def matches_module_boundary(imported_module: str, denied_module: str) -> bool:
    """Check if imported_module matches denied_module on exact module segments."""
    if imported_module == denied_module:
        return True
    if imported_module.startswith(denied_module + "."):
        return True
    return False


def matches_path_boundary(target_path: Path, denied_path: Path) -> bool:
    """Check if target_path is equal to or located within denied_path."""
    try:
        target_path.relative_to(denied_path)
        return True
    except ValueError:
        return False


def resolve_module_to_project_path(module_name: str, project_root: Path) -> Path | None:
    """Best-effort check if an absolute import refers to a file/package in project_root."""
    parts = module_name.split(".")
    candidate_py = project_root.joinpath(*parts).with_suffix(".py")
    if candidate_py.is_file():
        return candidate_py

    candidate_pkg = project_root.joinpath(*parts)
    if candidate_pkg.is_dir() and (candidate_pkg / "__init__.py").is_file():
        return candidate_pkg

    return None


def scan_file(file_path: Path, project_root: Path, active_rules: list[Rule]) -> list[Finding]:
    """Scan a single Python file against active boundary rules."""
    findings: list[Finding] = []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError) as e:
        # File syntax/encoding error is reported as an error violation to avoid silent passes
        rel_path = file_path.relative_to(project_root).as_posix()
        findings.append(
            Finding(
                status="violation",
                severity="error",
                rule_name="syntax-validation",
                file_path=rel_path,
                line=getattr(e, "lineno", 1) or 1,
                message=f"Failed to parse source file: {e}",
            )
        )
        return findings

    extractor = ImportExtractor(file_path, project_root)
    extractor.visit(tree)
    rel_file_str = file_path.relative_to(project_root).as_posix()

    for item_type, val, lineno in extractor.discovered:
        if item_type == "unresolved":
            for rule in active_rules:
                findings.append(
                    Finding(
                        status="unresolved",
                        severity="warning",
                        rule_name=rule.name,
                        file_path=rel_file_str,
                        line=lineno,
                        message="Non-constant dynamic import cannot be resolved statically.",
                    )
                )
            continue

        if item_type == "module":
            imported_mod = str(val)
            # 1. Check against deny_modules
            for rule in active_rules:
                for denied_mod in rule.deny_modules:
                    if matches_module_boundary(imported_mod, denied_mod):
                        findings.append(
                            Finding(
                                status="violation",
                                severity=rule.severity,
                                rule_name=rule.name,
                                file_path=rel_file_str,
                                line=lineno,
                                message=f"{rule.message} (denied module '{denied_mod}')",
                                imported=imported_mod,
                            )
                        )

            # 2. Check if this module actually maps to an internal deny_path
            resolved_internal = resolve_module_to_project_path(imported_mod, project_root)
            if resolved_internal:
                for rule in active_rules:
                    for denied_p in rule.deny_paths:
                        if matches_path_boundary(resolved_internal, denied_p):
                            rel_denied = denied_p.relative_to(project_root).as_posix()
                            findings.append(
                                Finding(
                                    status="violation",
                                    severity=rule.severity,
                                    rule_name=rule.name,
                                    file_path=rel_file_str,
                                    line=lineno,
                                    message=f"{rule.message} (denied path '{rel_denied}')",
                                    imported=imported_mod,
                                )
                            )

        elif item_type == "relative_resolved_path":
            resolved_p = val
            for rule in active_rules:
                for denied_p in rule.deny_paths:
                    if matches_path_boundary(resolved_p, denied_p):
                        rel_denied = denied_p.relative_to(project_root).as_posix()
                        findings.append(
                            Finding(
                                status="violation",
                                severity=rule.severity,
                                rule_name=rule.name,
                                file_path=rel_file_str,
                                line=lineno,
                                message=f"{rule.message} (denied path '{rel_denied}')",
                                imported=str(resolved_p.relative_to(project_root).as_posix()),
                            )
                        )

    return findings


def is_excluded(path: Path) -> bool:
    """Check if any path component is in the exclude set."""
    return any(part in DEFAULT_EXCLUDES for part in path.parts)


def run_validation(config_path: Path) -> tuple[int, list[Finding]]:
    """Run full boundary validation given a config file path."""
    project_root, rules = parse_config(config_path)

    all_findings: list[Finding] = []

    for file_path in project_root.rglob("*.py"):
        if is_excluded(file_path):
            continue

        resolved_file = file_path.resolve()
        # Find which rules apply to this file (file resides under rule.from_path)
        matching_rules = [
            r for r in rules if matches_path_boundary(resolved_file, r.from_path)
        ]

        if not matching_rules:
            continue

        file_findings = scan_file(resolved_file, project_root, matching_rules)
        all_findings.extend(file_findings)

    # Determine exit code:
    # 1 if any error severity violation exists
    # 0 if only warnings / unresolved or clean
    has_error = any(f.severity == "error" and f.status == "violation" for f in all_findings)
    exit_code = 1 if has_error else 0

    return exit_code, all_findings


def format_text_report(findings: list[Finding]) -> str:
    """Render human-readable text output."""
    if not findings:
        return "✓ All boundary checks passed. No violations found."

    lines: list[str] = []
    errors = [f for f in findings if f.severity == "error" and f.status == "violation"]
    warnings = [f for f in findings if f.severity == "warning" or f.status == "unresolved"]

    for f in findings:
        tag = f"[{f.severity.upper()}]"
        imported_str = f" (import: '{f.imported}')" if f.imported else ""
        lines.append(f"{tag} {f.rule_name} | {f.file_path}:{f.line} -> {f.message}{imported_str}")

    lines.append("")
    lines.append(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)/unresolved.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate architectural boundaries for SaaS/F4A projects.")
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        default=Path("f4a-boundaries.toml"),
        help="Path to f4a-boundaries.toml (default: ./f4a-boundaries.toml)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output findings in JSON format.",
    )

    args = parser.parse_args()

    try:
        exit_code, findings = run_validation(args.config)
    except Exception as e:
        sys.stderr.write(f"Configuration or execution error: {e}\n")
        return 2

    if args.json:
        report = {
            "exit_code": exit_code,
            "findings": [asdict(f) for f in findings],
            "total_errors": sum(1 for f in findings if f.severity == "error" and f.status == "violation"),
            "total_warnings": sum(1 for f in findings if f.severity == "warning" or f.status == "unresolved"),
        }
        print(json.dumps(report, indent=2))
    else:
        print(format_text_report(findings))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

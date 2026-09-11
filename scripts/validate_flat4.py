#!/usr/bin/env python3
"""Conservative static dependency checker for Pardpro Flat-4 projects."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SOURCE_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".h", ".hpp", ".java",
    ".js", ".jsx", ".kt", ".kts", ".mjs", ".py", ".rs", ".ts", ".tsx",
}
IGNORED_DIRECTORIES = {
    ".git", ".idea", ".next", ".venv", ".vscode", "build", "coverage",
    "dist", "node_modules", "target", "vendor", "venv",
}
LAYER_SEGMENTS = {
    "L0": {"l0", "l0-domain", "l0_domain", "domain"},
    "L1": {"l1", "l1-entry", "l1_entry", "entry"},
    "L2": {"l2", "l2-coordinator", "l2_coordinator", "coordinator"},
    "L3": {"l3", "l3-molecular", "l3_molecular", "molecular"},
    "L4": {"l4", "l4-atomic", "l4_atomic", "atomic"},
    "UTILS": {"utils", "common"},
}
ALLOWED_TARGETS = {
    "L0": {"UTILS"},
    "L1": {"L2", "L4", "UTILS"},
    "L2": {"L0", "L3", "L4", "UTILS"},
    "L3": {"L4", "UTILS"},
    "L4": {"UTILS"},
    "UTILS": {"UTILS"},
}
REFERENCE_PATTERN = re.compile(
    r"(?i)(?:^|[\\/._-])(l[0-4]|utils|common)(?:[\\/._-]|$)|"
    r"\b(l0_domain|l1_entry|l2_coordinator|l3_molecular|l4_atomic|utils|common)\b"
)
CONTROL_FLOW_PATTERN = re.compile(r"(?m)^\s*(if|elif|else|switch|case|for|while)\b")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    file: str
    line: int
    message: str


def normalize_segment(segment: str) -> str:
    return segment.casefold().replace(" ", "-")


def layer_from_path(path: Path) -> str | None:
    for segment in path.parts:
        normalized = normalize_segment(segment)
        for layer, aliases in LAYER_SEGMENTS.items():
            if normalized in aliases:
                return layer
    return None


def referenced_layers(line: str) -> set[str]:
    layers: set[str] = set()
    for match in REFERENCE_PATTERN.finditer(line):
        token = next(group for group in match.groups() if group)
        prefix = token.casefold().split("_")[0].upper()
        if prefix == "COMMON":
            prefix = "UTILS"
        layers.add(prefix)
    return layers


def is_source_file(path: Path) -> bool:
    return path.suffix.casefold() in SOURCE_EXTENSIONS and not any(
        part.casefold() in IGNORED_DIRECTORIES for part in path.parts
    )


import ast

def analyze_python_ast(text: str, relative_path: Path, source_layer: str, findings: list[Finding]):
    try:
        tree = ast.parse(text, filename=str(relative_path))
    except Exception as exc:
        findings.append(Finding("warning", "ast-parse-error", str(relative_path), 0, f"AST Parse Error: {exc}"))
        return

    class Flat4Visitor(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                self.check_reference(alias.name, node.lineno)
            self.generic_visit(node)
            
        def visit_ImportFrom(self, node):
            if node.module:
                self.check_reference(node.module, node.lineno)
            self.generic_visit(node)
            
        def visit_Name(self, node):
            self.check_reference(node.id, node.lineno)
            self.generic_visit(node)
            
        def check_reference(self, text: str, lineno: int):
            for target_layer in referenced_layers(text):
                if target_layer == source_layer or target_layer not in ALLOWED_TARGETS[source_layer]:
                    findings.append(Finding(
                        "error",
                        "illegal-layer-reference-ast",
                        str(relative_path),
                        lineno,
                        f"[AST Deep Scan] {source_layer} references {target_layer}; allowed targets: "
                        f"{', '.join(sorted(ALLOWED_TARGETS[source_layer])) or 'none'}.",
                    ))
    
    Flat4Visitor().visit(tree)


def scan(root: Path) -> tuple[list[Finding], dict[str, int]]:
    findings: list[Finding] = []
    counts = {layer: 0 for layer in LAYER_SEGMENTS}
    layered_files = 0

    for path in sorted(p for p in root.rglob("*") if p.is_file() and is_source_file(p)):
        relative = path.relative_to(root)
        source_layer = layer_from_path(relative)
        if source_layer is None:
            continue
        layered_files += 1
        counts[source_layer] += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append(Finding("warning", "unreadable-file", str(relative), 0, str(exc)))
            continue

        if path.suffix.casefold() == ".py":
            # Deep AST Scan for Python
            analyze_python_ast(text, relative, source_layer, findings)
        else:
            # Fallback regex scan for other languages
            for line_number, line in enumerate(text.splitlines(), start=1):
                for target_layer in referenced_layers(line):
                    if target_layer == source_layer or target_layer not in ALLOWED_TARGETS[source_layer]:
                        findings.append(Finding(
                            "error",
                            "illegal-layer-reference",
                            str(relative),
                            line_number,
                            f"{source_layer} references {target_layer}; allowed targets: "
                            f"{', '.join(sorted(ALLOWED_TARGETS[source_layer])) or 'none'}.",
                        ))

        if source_layer == "L1" and CONTROL_FLOW_PATTERN.search(text):
            line_number = text[:CONTROL_FLOW_PATTERN.search(text).start()].count("\n") + 1
            findings.append(Finding(
                "warning",
                "l1-control-flow",
                str(relative),
                line_number,
                "L1 contains control flow; verify that it is request parsing or startup logic, not business policy.",
            ))

    if layered_files == 0:
        findings.append(Finding(
            "warning",
            "no-layered-source",
            ".",
            0,
            "No source files were found under recognizable L0-L4 directories.",
        ))
    else:
        for required in ("L1", "L2", "L4"):
            if counts[required] == 0:
                findings.append(Finding(
                    "warning",
                    "missing-layer",
                    ".",
                    0,
                    f"No source files were found for required layer {required}.",
                ))

    unique = list(dict.fromkeys(findings))
    return unique, counts


def print_text(root: Path, findings: list[Finding], counts: dict[str, int]) -> None:
    print(f"Flat-4 static audit: {root}")
    print("Layered source files: " + ", ".join(f"{key}={value}" for key, value in counts.items()))
    if not findings:
        print("PASS: no static layer violations found.")
        print("Manual review is still required for state ownership and behavioral responsibilities.")
        return
    for finding in findings:
        location = finding.file if finding.line == 0 else f"{finding.file}:{finding.line}"
        print(f"[{finding.severity.upper()}] {finding.code} {location} - {finding.message}")
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    print(f"Result: {errors} error(s), {warnings} warning(s).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Project root to inspect")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    root = args.project.resolve()
    if not root.is_dir():
        parser.error(f"project is not a directory: {root}")

    findings, counts = scan(root)
    if args.json:
        print(json.dumps({
            "root": str(root),
            "counts": counts,
            "findings": [asdict(item) for item in findings],
        }, ensure_ascii=False, indent=2))
    else:
        print_text(root, findings, counts)
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Reject CJK characters in canonical documentation, except the bilingual README."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

DOCUMENT_EXTENSIONS = {".md", ".txt", ".toml", ".yaml", ".yml"}
IGNORED_DIRECTORIES = {".git", ".local", "dist", "__pycache__"}
BILINGUAL_FILES = {Path("README.md")}
CJK_PATTERN = re.compile(
    "["
    "\u3400-\u4dbf"
    "\u4e00-\u9fff"
    "\uf900-\ufaff"
    "\U00020000-\U0002fa1f"
    "]"
)


@dataclass(frozen=True)
class Violation:
    path: str
    line: int
    excerpt: str


def documentation_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file()
        and path.suffix.casefold() in DOCUMENT_EXTENSIONS
        and not IGNORED_DIRECTORIES.intersection(path.relative_to(root).parts)
    )


def scan(root: Path) -> list[Violation]:
    violations: list[Violation] = []
    for path in documentation_files(root):
        relative = path.relative_to(root)
        if relative in BILINGUAL_FILES:
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if CJK_PATTERN.search(line):
                violations.append(Violation(str(relative), line_number, line.strip()[:120]))
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    violations = scan(root)
    if not violations:
        print("PASS: English-only canonical documentation contains no CJK characters; the bilingual README is excluded.")
        return 0

    print("FAIL: canonical documentation outside the bilingual README must be English. Keep Chinese working copies under .local/zh/.")
    for violation in violations:
        print(f"{violation.path}:{violation.line}: {violation.excerpt}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

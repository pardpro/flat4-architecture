#!/usr/bin/env python3
"""Build a deterministic, installable F4A Skill archive under dist/."""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path


SKILL_NAME = "f4a-engineering-governance"
INCLUDED_FILES = ("SKILL.md", "VERSION")
INCLUDED_DIRECTORIES = ("agents", "references", "scripts")
EXCLUDED_PARTS = {"__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def release_files(root: Path) -> list[Path]:
    files = [root / name for name in INCLUDED_FILES]
    for directory in INCLUDED_DIRECTORIES:
        files.extend(path for path in (root / directory).rglob("*") if path.is_file())
    return sorted(
        path for path in files
        if not EXCLUDED_PARTS.intersection(path.parts)
        and path.suffix.casefold() not in EXCLUDED_SUFFIXES
    )


def build_release(root: Path) -> tuple[Path, str]:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise ValueError("VERSION must not be empty")

    output_dir = root / "dist"
    output_dir.mkdir(exist_ok=True)
    archive_path = output_dir / f"{SKILL_NAME}-{version}.zip"

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in release_files(root):
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{SKILL_NAME}/{relative}", ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    (output_dir / f"{archive_path.name}.sha256").write_text(
        f"{digest}  {archive_path.name}\n", encoding="ascii"
    )
    return archive_path, digest


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    archive_path, digest = build_release(root)
    print(f"Created: {archive_path}")
    print(f"SHA256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

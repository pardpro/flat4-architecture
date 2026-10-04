from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_release import SKILL_NAME, build_release


class PackageReleaseTests(unittest.TestCase):
    def test_archive_has_installable_root_and_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "VERSION").write_text("1.2.3\n", encoding="utf-8")
            (root / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\n", encoding="utf-8")
            (root / "agents").mkdir()
            (root / "agents/openai.yaml").write_text("interface: {}\n", encoding="utf-8")
            (root / "references").mkdir()
            (root / "references/rules.md").write_text("# Rules\n", encoding="utf-8")
            (root / "scripts").mkdir()
            (root / "scripts/validate_flat4.py").write_text("pass\n", encoding="utf-8")
            (root / "scripts/package_release.py").write_text("pass\n", encoding="utf-8")

            archive_path, digest = build_release(root)

            self.assertEqual(64, len(digest))
            self.assertTrue(archive_path.with_name(archive_path.name + ".sha256").is_file())
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
                self.assertIn(f"{SKILL_NAME}/SKILL.md", names)
                self.assertIn(f"{SKILL_NAME}/agents/openai.yaml", names)
                self.assertIn(f"{SKILL_NAME}/scripts/validate_flat4.py", names)
                self.assertNotIn(f"{SKILL_NAME}/scripts/package_release.py", names)


if __name__ == "__main__":
    unittest.main()

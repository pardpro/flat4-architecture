from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_english_docs import scan


class EnglishDocumentationTests(unittest.TestCase):
    def test_english_documentation_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# English documentation\n", encoding="utf-8")
            self.assertEqual([], scan(root))

    def test_bilingual_root_readme_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# 中文 documentation\n", encoding="utf-8")
            self.assertEqual([], scan(root))

    def test_cjk_in_canonical_documentation_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "docs/guide.md"
            path.parent.mkdir(parents=True)
            path.write_text("# 中文 documentation\n", encoding="utf-8")
            violations = scan(root)
            self.assertEqual(1, len(violations))
            self.assertEqual(str(Path("docs/guide.md")), violations[0].path)

    def test_local_chinese_copy_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / ".local/zh/README.md"
            path.parent.mkdir(parents=True)
            path.write_text("# 中文副本\n", encoding="utf-8")
            self.assertEqual([], scan(root))


if __name__ == "__main__":
    unittest.main()

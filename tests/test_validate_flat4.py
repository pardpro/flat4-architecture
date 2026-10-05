from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.hardware_realtime.validate_flat4 import analyze_python_ast, scan


class Flat4ValidatorTests(unittest.TestCase):
    def test_valid_layers_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "src/L1_Entry/main.py", "from L2_Coordinator.flow import run\n")
            self._write(root, "src/L2_Coordinator/flow.py", "from L4_Atomic.read import read\n")
            self._write(root, "src/L4_Atomic/read.py", "def read(): return 1\n")
            findings, counts = scan(root)

        self.assertEqual([], findings)
        self.assertEqual(1, counts["L1"])
        self.assertEqual(1, counts["L2"])
        self.assertEqual(1, counts["L4"])

    def test_same_layer_reference_is_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "src/L4_Atomic/first.py", "from L4_Atomic.second import run\n")
            self._write(root, "src/L1_Entry/main.py", "from L2_Coordinator.flow import run\n")
            self._write(root, "src/L2_Coordinator/flow.py", "pass\n")
            findings, _ = scan(root)

        self.assertIn("illegal-layer-reference-ast", {item.code for item in findings})

    def test_relative_import_is_checked(self):
        findings = []
        analyze_python_ast(
            "from . import L4_Atomic\n",
            Path("src/L1_Entry/main.py"),
            "L1",
            findings,
        )
        self.assertIn("l1-l4-query-review", {item.code for item in findings})

    def test_l0_io_import_requires_review(self):
        findings = []
        analyze_python_ast(
            "import os\nos.remove('file')\n",
            Path("src/L0_Domain/rules.py"),
            "L0",
            findings,
        )
        self.assertIn("l0-io-import-review", {item.code for item in findings})

    @staticmethod
    def _write(root: Path, relative: str, content: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()

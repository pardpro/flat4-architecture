import tempfile
import unittest
from pathlib import Path

from scripts.saas.validate_boundaries import (
    matches_module_boundary,
    matches_path_boundary,
    run_validation,
)


class BoundaryValidatorTests(unittest.TestCase):
    def test_module_boundary_matching(self):
        # Exact match
        self.assertTrue(matches_module_boundary("stripe", "stripe"))
        # Submodule match
        self.assertTrue(matches_module_boundary("stripe.checkout", "stripe"))
        self.assertTrue(matches_module_boundary("stripe.api.v1", "stripe"))
        # Should NOT match different module with prefix
        self.assertFalse(matches_module_boundary("stripe_helpers", "stripe"))
        self.assertFalse(matches_module_boundary("stripeme", "stripe"))
        self.assertFalse(matches_module_boundary("django_extensions", "django"))

    def test_path_boundary_matching(self):
        root = Path("/app/src")
        infra = root / "infrastructure"
        db = infra / "database" / "models.py"
        domain = root / "domain" / "user.py"

        self.assertTrue(matches_path_boundary(db, infra))
        self.assertFalse(matches_path_boundary(domain, infra))

    def test_validation_workflow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            src = tmppath / "src"
            domain = src / "domain"
            web = src / "interfaces" / "web"
            infra = src / "infrastructure"

            domain.mkdir(parents=True)
            web.mkdir(parents=True)
            infra.mkdir(parents=True)

            # Create sample files
            (domain / "user.py").write_text(
                "import stripe_helpers\n"  # allowed (not stripe)
                "import stripe\n"          # violation: deny_modules
                "from infrastructure import db\n"  # violation: deny_paths
                "import importlib\n"
                "mod = importlib.import_module('openai')\n"  # constant dynamic violation
                "dynamic_mod = importlib.import_module(some_var)\n",  # unresolved
                encoding="utf-8",
            )

            (web / "handler.py").write_text(
                "from ..domain import user\n"  # allowed relative
                "import django\n",             # allowed in web (only banned in domain)
                encoding="utf-8",
            )

            config = tmppath / "f4a-boundaries.toml"
            config.write_text(
                """
version = 1

[project]
root = "src"

[[rules]]
name = "domain-purity"
from = "domain"
deny_modules = ["stripe", "openai"]
deny_paths = ["infrastructure"]
severity = "error"
message = "Domain must remain clean."

[[rules]]
name = "web-no-direct-db"
from = "interfaces/web"
deny_paths = ["infrastructure/database"]
severity = "error"
message = "Web cannot access database directly."
""",
                encoding="utf-8",
            )

            exit_code, findings = run_validation(config)

            # Exit code must be 1 due to errors in domain/user.py
            self.assertEqual(exit_code, 1)

            # Check that stripe_helpers is NOT among findings
            imported_names = [f.imported for f in findings if f.imported]
            self.assertIn("stripe", imported_names)
            self.assertIn("openai", imported_names)
            self.assertNotIn("stripe_helpers", imported_names)

            # Check for unresolved finding
            unresolved = [f for f in findings if f.status == "unresolved"]
            self.assertTrue(len(unresolved) >= 1)
            self.assertEqual(unresolved[0].severity, "warning")

    def test_clean_project_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            src = tmppath / "src"
            domain = src / "domain"
            domain.mkdir(parents=True)

            (domain / "entity.py").write_text("import math\n", encoding="utf-8")

            config = tmppath / "f4a-boundaries.toml"
            config.write_text(
                """
version = 1
[project]
root = "src"

[[rules]]
name = "domain-purity"
from = "domain"
deny_modules = ["django"]
severity = "error"
""",
                encoding="utf-8",
            )

            exit_code, findings = run_validation(config)
            self.assertEqual(exit_code, 0)
            self.assertEqual(len(findings), 0)


if __name__ == "__main__":
    unittest.main()

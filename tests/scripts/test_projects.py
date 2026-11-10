"""projects.py parses every PROJECTS.md row (task 2.7). Run: python3 -m unittest discover tests/scripts"""
import importlib.util, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("projects", ROOT / "skills/judo-catalog-maintain/scripts/projects.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class ProjectsTest(unittest.TestCase):
    def test_every_row_parses(self):
        rows, errs = mod.parse((ROOT / "PROJECTS.md").read_text())
        self.assertEqual(errs, [])
        self.assertGreaterEqual(len(rows), 21)
        self.assertRegex({r["Project"]: r["Swept SHA"] for r in rows}["mlszksz-platform"], r"^[0-9a-f]{7,40}$")
        self.assertRegex({r["Project"]: r["Swept SHA"] for r in rows}["rackinspect"], r"^([0-9a-f]{7,40}|unreachable)$")

    def test_bad_kind_is_reported(self):
        txt = "| # | Project | Git URL | Kind | Branch | Swept SHA | First Commit | Last Commit | Commits | Weight [-10;+10] |\n|---|---|---|---|---|---|---|---|---|---|\n| 1 | **x** | u | lib | develop | - | a | b | 1 | 0 |"
        _, errs = mod.parse(txt)
        self.assertTrue(any("Kind" in e for e in errs))

if __name__ == "__main__":
    unittest.main()

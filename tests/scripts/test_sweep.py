"""Sweep script tests on fixture data (task 7.1b). Run: python3 -m unittest discover tests/scripts"""
import json, pathlib, subprocess, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[2]
S = ROOT / "skills/judo-catalog-maintain/scripts"

def run(*a, **kw):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True, **kw)

class OverlapTest(unittest.TestCase):
    def test_shared_entry_is_listed(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            for proj, entries in (("alpha", ["audit-log-entity", "soft-delete-active-flag"]),
                                  ("beta", ["model-blueprints/audit-log-entity", "best-practices/model/enum-state-machine.md"])):
                w = root / proj / "abc1234"; w.mkdir(parents=True)
                (w / "decisions.json").write_text(json.dumps({"decisions": [
                    {"name": e, "decision": "add-evidence", "entry": e} for e in entries]}))
            r = run(S / "sweep-overlap", "--root", root, "--json")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout), {"audit-log-entity": ["alpha", "beta"]})

    def test_rejected_decisions_do_not_overlap(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            for proj, dec in (("alpha", "add-evidence"), ("beta", "reject")):
                w = root / proj / "abc1234"; w.mkdir(parents=True)
                (w / "decisions.json").write_text(json.dumps({"decisions": [{"name": "x", "decision": dec, "entry": "x"}]}))
            self.assertEqual(json.loads(run(S / "sweep-overlap", "--root", root, "--json").stdout), {})

class MergeTest(unittest.TestCase):
    def test_lanes_join_on_shared_element(self):
        import importlib.util, sys
        sys.path.insert(0, str(S))
        spec = importlib.util.spec_from_file_location("sm", S / "sweep-merge", loader=None)
        # run through the CLI on a temporary work folder under target/sweep
        w = ROOT / "target/sweep/_fixture/0000000"; (w / "lanes").mkdir(parents=True, exist_ok=True)
        (w / "state.json").write_text(json.dumps({"project": "_fixture", "sha": "0" * 40}))
        (w / "lanes/model.json").write_text(json.dumps({"candidates": [
            {"name": "Header Line", "kind": "blueprint", "domain": "model", "elements": ["m::Order"], "summary": "header/line", "match": "x", "match_score": 0.4}]}))
        (w / "lanes/backend.json").write_text(json.dumps({"candidates": [
            {"name": "range-interceptor", "kind": "practice", "domain": "backend", "elements": ["m::Order"], "summary": "range", "match": "y", "match_score": 0.9}]}))
        try:
            r = run(S / "sweep-merge", "_fixture", "--json")
            self.assertEqual(r.returncode, 0, r.stderr)
            c = json.loads((w / "candidates.json").read_text())
            self.assertEqual(len(c["candidates"]), 1)
            self.assertEqual(c["candidates"][0]["lanes"], ["backend", "model"])
            self.assertEqual(c["candidates"][0]["match"], "y")
            self.assertEqual(sorted(c["missing_lanes"]), ["frontend", "schema"])
        finally:
            import shutil; shutil.rmtree(ROOT / "target/sweep/_fixture")

if __name__ == "__main__":
    unittest.main()

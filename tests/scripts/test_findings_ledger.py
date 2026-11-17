import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOL = ROOT / ".pi/skills/judo-catalog-expand/scripts/findings-ledger"


def write(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))


class ReconcileTest(unittest.TestCase):
    def run_tool(self, w):
        return subprocess.run([str(TOOL), "reconcile", str(w)], capture_output=True, text=True)

    def test_every_finding_must_be_accounted_for(self):
        with tempfile.TemporaryDirectory() as d:
            w = pathlib.Path(d)
            write(w / "inventory.jsonl", [{"id": "A", "src": "s", "target": "t.md", "text": "a"},
                                          {"id": "B", "src": "s", "target": "t.md", "text": "b"},
                                          {"id": "C", "src": "s", "target": "t.md", "text": "c"}])
            write(w / "ledger/x.jsonl", [{"id": "A", "status": "applied"}, {"id": "C", "status": "unverified"}])
            r = self.run_tool(w)
            self.assertEqual(r.returncode, 1)
            self.assertIn("UNACCOUNTED B: MISSING", r.stdout)
            self.assertIn("UNACCOUNTED A: APPLIED-UNCHECKED", r.stdout)
            self.assertIn("UNACCOUNTED C: UNVERIFIED-NOT-RESEARCHED", r.stdout)

    def test_resolved_pass(self):
        with tempfile.TemporaryDirectory() as d:
            w = pathlib.Path(d)
            write(w / "inventory.jsonl", [{"id": "A", "src": "s", "target": "t.md", "text": "a"},
                                          {"id": "B", "src": "s", "target": "t.md", "text": "b"}])
            write(w / "ledger/x.jsonl", [{"id": "A", "status": "applied"}, {"id": "B", "status": "unverified"},
                                         {"id": "B", "status": "handoff"}])
            write(w / "research/r.out.jsonl", [{"id": "B", "status": "open", "evidence": "no source"}])
            write(w / "check/x.jsonl", [{"id": "A", "verdict": "ok"}])
            r = self.run_tool(w)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("| B |", (w / "OPEN-ITEMS.md").read_text())


if __name__ == "__main__":
    unittest.main()


class RawCoverageTest(unittest.TestCase):
    def test_raw_rows_outside_inventory_fail(self):
        with tempfile.TemporaryDirectory() as d:
            w = pathlib.Path(d)
            write(w / "inventory.jsonl", [{"id": "A", "src": "s", "target": "t.md", "text": "a"}])
            write(w / "ledger/x.jsonl", [{"id": "A", "status": "already-correct"}])
            write(w / "raw.jsonl", [{"id": "R1", "kind": "doc", "covered_by": "A"},
                                    {"id": "R2", "kind": "bug", "covered_by": None},
                                    {"id": "R3", "kind": "bug", "covered_by": None}])
            write(w / "triage/verdicts-1.jsonl", [{"id": "R3", "verdict": "not-platform"}])
            r = subprocess.run([str(TOOL), "reconcile", str(w)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("UNACCOUNTED R2: RAW-UNTRIAGED", r.stdout)
            self.assertNotIn("R3", r.stdout.split("raw")[0])
            self.assertIn("Raw source coverage", (w / "SUMMARY.md").read_text())

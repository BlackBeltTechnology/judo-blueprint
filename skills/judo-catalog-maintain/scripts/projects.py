#!/usr/bin/env python3
"""Read and check PROJECTS.md, the registry of projects the catalog was taken from (tasks 2.4, 2.7).

Usage:
  projects.py list [--json]      print the registry rows
  projects.py check [--json]     every `projects:` value in catalog entries must be a registry name;
                                 every row must parse; exit 1 on problems
  projects.py usage [--json]     catalog entries per project

PROJECTS.md table columns: # | Project | Git URL | Kind | Branch | Swept SHA | First Commit | Last Commit | Commits | Weight [-10;+10]
`Kind` is `app` or `demo`; `Branch` is the branch the catalog was taken from; `Swept SHA` is the last commit swept
(`-` = not swept, `unreachable` = the recorded SHA no longer exists). Read-only: never clones, fetches or pushes.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
COLS = ["#", "Project", "Git URL", "Kind", "Branch", "Swept SHA", "First Commit", "Last Commit", "Commits", "Weight"]


def parse(text):
    rows, errs = [], []
    lines = [l for l in text.split("\n") if l.startswith("|")]
    if not lines:
        return rows, ["no table"]
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    if [h.split(" [")[0] for h in head] != COLS:
        errs.append(f"header mismatch: {head}")
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) != len(COLS):
            errs.append(f"bad row ({len(cells)} cells): {l[:80]}")
            continue
        r = dict(zip(COLS, cells))
        r["Project"] = r["Project"].strip("*")
        try:
            r["Weight"] = int(r["Weight"])
        except ValueError:
            errs.append(f"{r['Project']}: weight not an integer")
        if r["Kind"] not in ("app", "demo"):
            errs.append(f"{r['Project']}: Kind must be app or demo, got {r['Kind']!r}")
        if not re.fullmatch(r"-|unreachable|[0-9a-f]{7,40}", r["Swept SHA"]):
            errs.append(f"{r['Project']}: Swept SHA must be -, unreachable or a SHA")
        rows.append(r)
    return rows, errs


def entry_projects():
    out = {}
    cat = ROOT / "catalog"
    files = list(cat.glob("model-blueprints/*/BLUEPRINT.md")) + [
        p for p in cat.glob("best-practices/*/*.md") if p.name not in ("README.md", "AGENTS.md")]
    for p in files:
        m = re.search(r"^projects:\s*\[(.*?)\]", p.read_text(), re.M)
        if m:
            out[str(p.relative_to(ROOT))] = [x.strip().strip("\"'") for x in m.group(1).split(",") if x.strip()]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["list", "check", "usage"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rows, errs = parse((ROOT / "PROJECTS.md").read_text())
    names = {r["Project"] for r in rows}
    if a.cmd == "list":
        print(json.dumps(rows, indent=1) if a.json else "\n".join(f"{r['Project']:28} {r['Kind']:5} {r['Branch']:10} {r['Swept SHA']}" for r in rows))
        return 1 if errs else 0
    ep = entry_projects()
    if a.cmd == "usage":
        use = {n: 0 for n in names}
        for ps in ep.values():
            for p in ps:
                use[p] = use.get(p, 0) + 1
        print(json.dumps(use, indent=1) if a.json else "\n".join(f"{v:4} {k}" for k, v in sorted(use.items(), key=lambda x: -x[1])))
        return 0
    for f, ps in ep.items():
        for p in ps:
            if p not in names:
                errs.append(f"{f}: project {p!r} not in PROJECTS.md")
    if a.json:
        print(json.dumps({"rows": len(rows), "errors": errs}))
    else:
        print("\n".join(errs) or f"ok: {len(rows)} projects, {len(ep)} entries")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())

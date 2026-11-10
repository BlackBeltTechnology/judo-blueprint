#!/usr/bin/env python3
"""Merge every sweep knowledge source into one inventory, grouped by target.

Usage: merge.py [--out target/mining/inventory]

Sources (all under target/ unless noted):
  S1 mining/out/*.json                 session-mined items (decisions, corrections, wrong facts, missing, bugs, workflow)
  S2 judo-ng-read/findings_rows.json   2864 judo-ng findings [kind, repo, location, claim, fact]
  S3 agent-docs-review/<area>.json     per-area agent-docs verification findings
  S4 gap-mining/all_gaps.json          420 knowledge gaps
  S5 change folder md: judo-doc-problems.md, catalog-update-report.md, knowledge-gaps-report.md,
     judo-knowledge-reference.md, review-decisions*.md, judo-knowledge-decisions.md (section index only)

Writes:
  inventory/all.jsonl              one normalized row per item: {src, kind, area, target, topic, claim, fact, evidence, status}
  inventory/by-target/<slug>.md    rows grouped per target file / area for the doc-update agents
  inventory/summary.md             counts per source, kind, target
"""
import argparse
import collections
import glob
import json
import os
import re

T = "target"
CH = "openspec/changes/restructure-blueprints-for-kb"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "unknown").lower()).strip("-")[:80] or "unknown"


AREAS = ("model", "backend", "frontend", "deployment", "integration-testing", "e2e-testing")


def norm_target(t, area):
    t = (t or "").strip().split(" ")[0].rstrip(",;")
    if t.startswith("catalog/agent-docs/"):
        t = t[len("catalog/"):]
    if t.startswith("agent-docs"):
        t = re.sub(r"\.hbs$", "", t).rstrip("/")
        parts = t.split("/")
        if len(parts) >= 2 and parts[1].endswith(".md") and parts[1][:-3] in AREAS:
            return f"agent-docs/{parts[1][:-3]}"
        if len(parts) >= 2 and parts[1] in AREAS:
            if len(parts) >= 3 and parts[2].endswith(".md"):
                return f"agent-docs/{parts[1]}/{parts[2]}"
            return f"agent-docs/{parts[1]}"
        a2 = (area or "").lower()
        return f"agent-docs/{a2}" if a2 in AREAS else "agent-docs/(general)"
    if t.startswith(("catalog/model-blueprints", "catalog/best-practices", "judo-ng/", "skill/")):
        return "/".join(t.split("/")[:3])
    if t in ("change-process", "unknown", ""):
        return f"area/{area or 'other'}"
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=f"{T}/mining/inventory")
    a = ap.parse_args()
    os.makedirs(f"{a.out}/by-target", exist_ok=True)
    rows = []
    # S1
    for f in sorted(glob.glob(f"{T}/mining/out/*.json")):
        d = json.load(open(f))
        for x in d.get("items", []):
            rows.append({"src": "session:" + os.path.basename(f), **{k: x.get(k) for k in ("kind", "area", "target", "topic", "claim", "fact", "evidence", "status")}})
    # S2
    for r in json.load(open(f"{T}/judo-ng-read/findings_rows.json")):
        kind, repo, loc, claim, fact = (r + [None] * 5)[:5]
        rows.append({"src": "judo-ng-read", "kind": {"doc": "wrong-fact", "dox": "wrong-fact"}.get(kind, kind), "area": "judo-ng",
                     "target": f"judo-ng/{repo}", "topic": loc, "claim": claim, "fact": fact, "evidence": f"{repo}:{loc}", "status": "validated"})
    # S3
    for f in glob.glob(f"{T}/agent-docs-review/*.json"):
        d = json.load(open(f))
        for x in d.get("findings", []) if isinstance(d, dict) else []:
            rows.append({"src": "agent-docs-review:" + os.path.basename(f), "kind": x.get("kind") or x.get("type") or "wrong-fact",
                         "area": d.get("area"), "target": "agent-docs/" + str(x.get("doc") or x.get("file") or d.get("area")),
                         "topic": x.get("title") or x.get("heading") or x.get("id"), "claim": x.get("claim") or x.get("doc_says"),
                         "fact": x.get("fact") or x.get("reality") or x.get("correct"), "evidence": x.get("evidence") or x.get("source"),
                         "status": x.get("status") or "reported", "raw": x})
    # S4
    for x in json.load(open(f"{T}/gap-mining/all_gaps.json")):
        rows.append({"src": "gap-mining", "kind": x.get("kind", "missing"), "area": x.get("area"), "target": x.get("target"),
                     "topic": x.get("title"), "claim": None, "fact": x.get("what"), "evidence": x.get("evidence") or x.get("sources"),
                     "status": x.get("status", "mined")})
    # S5 section index (the md reports are already curated; agents read them in full)
    for name in ["judo-doc-problems.md", "catalog-update-report.md", "knowledge-gaps-report.md", "judo-knowledge-reference.md",
                 "judo-knowledge-decisions.md", "review-decisions.md", "review-decisions.boti.md", "review-decisions.gabor.md", "missing-topics.md"]:
        p = f"{CH}/{name}"
        if not os.path.exists(p):
            continue
        stack = []
        for i, line in enumerate(open(p), 1):
            m = re.match(r"^(#{1,4}) (.+)", line)
            if m:
                lvl = len(m.group(1))
                stack = stack[: lvl - 1] + [m.group(2).strip()]
                if lvl >= 2:
                    rows.append({"src": "report:" + name, "kind": "section", "area": stack[1] if len(stack) > 1 else None,
                                 "target": "report", "topic": " > ".join(stack), "claim": None, "fact": None,
                                 "evidence": f"{p}:{i}", "status": "curated"})
    for r in rows:
        r["target_key"] = norm_target(r.get("target"), r.get("area"))
    with open(f"{a.out}/all.jsonl", "w") as o:
        for r in rows:
            o.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
    groups = collections.defaultdict(list)
    for r in rows:
        if r["kind"] != "section":
            groups[r["target_key"]].append(r)
    for k, rs in groups.items():
        with open(f"{a.out}/by-target/{slug(k)}.md", "w") as o:
            o.write(f"# {k} ({len(rs)} items)\n\n")
            for r in rs:
                o.write(f"## [{r['kind']}] {r.get('topic') or ''}\n- src: {r['src']} | status: {r.get('status')} | evidence: {r.get('evidence')}\n")
                if r.get("claim"):
                    o.write(f"- claim: {r['claim']}\n")
                if r.get("fact"):
                    o.write(f"- fact: {r['fact']}\n")
                o.write("\n")
    by_src = collections.Counter(r["src"].split(":")[0] for r in rows)
    by_kind = collections.Counter(r["kind"] for r in rows)
    by_t = collections.Counter(r["target_key"] for r in rows if r["kind"] != "section")
    with open(f"{a.out}/summary.md", "w") as o:
        o.write("# Sweep inventory\n\n## By source\n" + "".join(f"- {k}: {v}\n" for k, v in by_src.most_common()))
        o.write("\n## By kind\n" + "".join(f"- {k}: {v}\n" for k, v in by_kind.most_common()))
        o.write("\n## By target\n" + "".join(f"- {k}: {v}\n" for k, v in by_t.most_common()))
    print(f"rows={len(rows)} targets={len(groups)}")
    print("by src", dict(by_src))
    print("by kind", dict(by_kind.most_common(10)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Coverage check for session mining: every chunk must have an output whose windows cover all lines.

Usage: coverage.py [--root target/mining] [--json]
Prints per chunk: status (missing|partial|ok), lines covered / total, items.
Exit 1 when any chunk is not ok. `todo` lists chunk names to (re)mine.
"""
import argparse
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="target/mining")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sess = os.path.join(a.root, "sessions")
    out = os.path.join(a.root, "out")
    by_chunk = {}
    for f in os.listdir(out) if os.path.isdir(out) else []:
        if not f.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(out, f)))
        except Exception:
            continue
        by_chunk.setdefault(os.path.basename(d.get("chunk", "")), []).append((f, d))
    rows, todo = [], []
    for c in sorted(x for x in os.listdir(sess) if x.endswith(".md")):
        total = sum(1 for _ in open(os.path.join(sess, c)))
        best = None
        for f, d in by_chunk.get(c, []):
            covered = set()
            for w in d.get("windows", []):
                try:
                    lo, hi = int(w[0]), int(w[1])
                except Exception:
                    continue
                covered.update(range(max(1, lo), min(total, hi) + 1))
            r = (len(covered), len(d.get("items", [])), f)
            best = max(best, r) if best else r
        if not best:
            st = "missing"
            cov, items, f = 0, 0, ""
        else:
            cov, items, f = best
            st = "ok" if cov >= total else "partial"
        if st != "ok":
            todo.append(c)
        rows.append({"chunk": c, "status": st, "covered": cov, "total": total, "items": items, "output": f})
    if a.json:
        print(json.dumps({"rows": rows, "todo": todo}, indent=1))
    else:
        for r in rows:
            print(f"{r['status']:8} {r['covered']:5}/{r['total']:<5} items={r['items']:3} {r['chunk']}")
        print(f"ok={sum(r['status']=='ok' for r in rows)} partial={sum(r['status']=='partial' for r in rows)} missing={sum(r['status']=='missing' for r in rows)} items={sum(r['items'] for r in rows)}")
    return 1 if todo else 0


if __name__ == "__main__":
    raise SystemExit(main())

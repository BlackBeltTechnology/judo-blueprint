#!/usr/bin/env python3
"""Extract judo-blueprint sweep sessions into deduplicated, readable chunks for mining.

Usage: extract-sessions.py [--out target/mining/sessions] [--chunk-kb 160]

Reads every pi session JSONL that mentions the sweep artifacts, drops messages
already seen (forked sessions share history), and writes markdown chunks with:
user messages (full), assistant text (full), tool calls (name + short args),
tool results (Agent results full up to 12k chars, others cut to 1.5k).
Also writes index.json: chunk -> session, time range, message count.
"""
import argparse
import glob
import json
import os
import re

SESS = os.path.expanduser("~/.pi/agent/sessions")
PAT = re.compile(r"judo-doc-problems|catalog-update-report|knowledge-gaps-report|agent-docs-review|judo-ng-read|gap-mining")


def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    for c in content or []:
        if not isinstance(c, dict):
            continue
        t = c.get("type")
        if t == "text":
            out.append(c.get("text", ""))
        elif t == "toolCall":
            a = json.dumps(c.get("arguments", {}), ensure_ascii=False)
            out.append(f"[tool call {c.get('name')}] {a[:600]}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="target/mining/sessions")
    ap.add_argument("--chunk-kb", type=int, default=160)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    files = []
    for f in glob.glob(SESS + "/*/*.jsonl"):
        with open(f, errors="ignore") as fh:
            if PAT.search(fh.read()):
                files.append(f)
    files.sort(key=lambda f: (-os.path.getsize(f)))  # superset sessions first
    seen = set()
    index = []
    for f in files:
        sid = os.path.basename(f)[:40]
        proj = os.path.basename(os.path.dirname(f)).strip("-")
        buf, size, part, n, t0, t1 = [], 0, 0, 0, None, None

        def flush():
            nonlocal buf, size, part, n, t0, t1
            if not buf:
                return
            name = f"{proj[-30:]}__{sid[:24]}__{part:03d}.md"
            with open(os.path.join(a.out, name), "w") as o:
                o.write(f"# session {sid} ({proj}) part {part}\n\n" + "".join(buf))
            index.append({"chunk": name, "session": f, "part": part, "messages": n, "from": t0, "to": t1})
            buf, size, n, t0, t1 = [], 0, 0, None, None
            part += 1

        with open(f, errors="ignore") as fh:
            for line in fh:
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                if e.get("type") != "message":
                    continue
                mid = e.get("id")
                if mid in seen:
                    continue
                seen.add(mid)
                m = e.get("message") or {}
                role = m.get("role")
                ts = e.get("timestamp", "")
                body = text_of(m.get("content"))
                if role == "toolResult":
                    lim = 12000 if m.get("toolName") == "Agent" or m.get("toolName") == "AgentStatus" else 1500
                    if len(body) > lim:
                        body = body[: lim // 2] + f"\n[… {len(body) - lim} chars cut …]\n" + body[-lim // 2:]
                    head = f"### tool result {m.get('toolName')} ({ts})\n"
                elif role == "user":
                    head = f"### USER ({ts})\n"
                elif role == "assistant":
                    head = f"### assistant ({ts})\n"
                else:
                    continue
                if not body.strip():
                    continue
                chunk = head + body.strip() + "\n\n"
                buf.append(chunk)
                size += len(chunk)
                n += 1
                t0 = t0 or ts
                t1 = ts
                if size > a.chunk_kb * 1024:
                    flush()
        flush()
    with open(os.path.join(a.out, "index.json"), "w") as o:
        json.dump(index, o, indent=1)
    print(f"sessions={len(files)} chunks={len(index)} unique_messages={len(seen)}")


if __name__ == "__main__":
    main()

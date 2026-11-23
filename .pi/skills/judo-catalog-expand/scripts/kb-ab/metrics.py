#!/usr/bin/env python3
"""metrics.py -> $KBAB_WORK/metrics.jsonl: one row per run listed in runs.txt, read from the session log.
Every kb_* tool counts as a kb call; weak kb_get = under 200 chars or 'not found'."""
import json, os, re, datetime, glob
ROOT = os.popen('git -C "%s" rev-parse --show-toplevel' % os.path.dirname(os.path.abspath(__file__))).read().strip()
WORK = os.environ.get('KBAB_WORK', f'{ROOT}/target/kbab')
TASKS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks.json')))
RUNS = {l.split()[3]: l.split()[:3] for l in open(f'{WORK}/runs.txt') if len(l.split()) == 4}
rows = []
for f in glob.glob(os.path.expanduser('~/.pi/agent/sessions/*/*.jsonl')):
    sid = re.search(r'([0-9a-f-]{36})\.jsonl$', f)
    if not sid or sid.group(1) not in RUNS: continue
    v, t, r = RUNS[sid.group(1)]
    L = [json.loads(l) for l in open(f)]
    calls, res, tok, cost, ts, answer = [], {}, 0, 0.0, [], ''
    for e in L:
        if e.get('timestamp'): ts.append(e['timestamp'])
        m = e.get('message') or {}
        if m.get('role') == 'assistant':
            u = m.get('usage') or {}; tok += u.get('totalTokens', 0); cost += (u.get('cost') or {}).get('total', 0)
            for x in m.get('content') or []:
                if isinstance(x, dict) and x.get('type') == 'toolCall': calls.append((x['id'], x['name']))
                if isinstance(x, dict) and x.get('type') == 'text' and x.get('text', '').strip(): answer = x['text']
        if m.get('role') == 'toolResult':
            res[m.get('toolCallId')] = ''.join(y.get('text', '') for y in (m.get('content') or []) if isinstance(y, dict))
    kb = [c for c in calls if c[1].startswith('kb_')]; kb_s = [c for c in kb if c[1] == 'kb_search']; kb_g = [c for c in kb if c[1] == 'kb_get']
    weak = sum(1 for c in kb_g if len(res.get(c[0], '').strip()) < 200 or 'not found' in res.get(c[0], '')[:80])
    t0, t1 = (datetime.datetime.fromisoformat(x.replace('Z', '+00:00')) for x in (ts[0], ts[-1]))
    rows.append({'variant': v, 'task': t, 'rep': int(r), 'id': sid.group(1), 'kb_search': len(kb_s), 'kb_get': len(kb_g),
                 'kb_other': len(kb) - len(kb_s) - len(kb_g), 'kb_calls': len(kb), 'other_tools': len(calls) - len(kb),
                 'kb_get_weak': weak, 'kb_bytes': sum(len(res.get(c[0], '')) for c in kb), 'tokens': tok, 'cost': round(cost, 4),
                 'seconds': int((t1 - t0).total_seconds()), 'answer': answer})
with open(f'{WORK}/metrics.jsonl', 'w') as o:
    for x in rows: o.write(json.dumps(x) + '\n')
print(len(rows), 'runs of', len(RUNS), 'listed;', sum(x['other_tools'] for x in rows), 'non-kb tool calls')

#!/usr/bin/env python3
"""metrics2.py -> metrics2.jsonl: round 2 (new kb), only sessions whose prompt carries a [run kbab-...] tag; every kb_* tool counts as a kb call."""
import json, glob, os, re, datetime
ROOT = '/Users/bmiller/Projects/judo-blueprint/target/kbab'
rows = []
TASKS = json.load(open(f'{ROOT}/tasks.json'))
for f in sorted(glob.glob(os.path.expanduser('~/.pi/agent/sessions/*kbab-*--/*.jsonl'))):
    v = re.search(r'kbab-(.+?)--', f).group(1); sid = re.search(r'_([0-9a-f-]{36})\.jsonl$', f).group(1); r = 0
    L = [json.loads(l) for l in open(f)]
    first = next(e for e in L if (e.get('message') or {}).get('role') == 'user')['message']['content']
    first = first if isinstance(first, str) else ''.join(x.get('text', '') for x in first if isinstance(x, dict))
    if '[run kbab-' not in first: continue
    t = next(k['id'] for k in TASKS if k['prompt'][:120] in first)
    calls, res, tok, cost, ts, answer = [], {}, 0, 0.0, [], ''
    for e in L:
        if e.get('timestamp'): ts.append(e['timestamp'])
        m = e.get('message') or {}
        if m.get('role') == 'assistant':
            u = m.get('usage') or {}
            tok += u.get('totalTokens', 0); cost += (u.get('cost') or {}).get('total', 0)
            for x in m.get('content') or []:
                if isinstance(x, dict) and x.get('type') == 'toolCall': calls.append((x['id'], x['name'], x.get('arguments')))
                if isinstance(x, dict) and x.get('type') == 'text' and x.get('text', '').strip(): answer = x['text']
        if m.get('role') == 'toolResult':
            res[m.get('toolCallId')] = ''.join(y.get('text', '') for y in (m.get('content') or []) if isinstance(y, dict))
    kb_s = [c for c in calls if c[1] == 'kb_search']; kb_g = [c for c in calls if c[1] == 'kb_get']; kb_o = [c for c in calls if c[1].startswith('kb_') and c[1] not in ('kb_search', 'kb_get')]
    kb_bytes = sum(len(res.get(c[0], '')) for c in kb_s + kb_g + kb_o)
    get_empty = sum(1 for c in kb_g if len(res.get(c[0], '').strip()) < 200 or 'not found' in res.get(c[0], '')[:80])
    t0 = datetime.datetime.fromisoformat(ts[0].replace('Z', '+00:00')); t1 = datetime.datetime.fromisoformat(ts[-1].replace('Z', '+00:00'))
    rows.append({'variant': v, 'task': t, 'rep': int(r), 'id': sid, 'kb_search': len(kb_s), 'kb_get': len(kb_g), 'kb_other': len(kb_o), 'kb_calls': len(kb_s) + len(kb_g) + len(kb_o),
                 'other_tools': len(calls) - len(kb_s) - len(kb_g) - len(kb_o), 'kb_get_weak': get_empty, 'kb_bytes': kb_bytes, 'tokens': tok, 'cost': round(cost, 4),
                 'seconds': int((t1 - t0).total_seconds()), 'answer': answer})
with open(f'{ROOT}/metrics2.jsonl', 'w') as o:
    for x in rows: o.write(json.dumps(x) + '\n')
print(len(rows), 'runs')

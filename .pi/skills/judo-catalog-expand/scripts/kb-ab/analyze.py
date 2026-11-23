#!/usr/bin/env python3
"""analyze.py <base> [--reps 1-4] [--grades grades.jsonl] -> markdown table: every variant against the SAME-BATCH baseline.
Ratios are per-task means divided by the baseline's per-task means, averaged over tasks; 95% CI by bootstrap.
With k variants at once, expect about k/20 false hits: confirm a winner in its own run decided in advance."""
import json, os, collections, statistics as S, random, argparse
ROOT = os.popen('git -C "%s" rev-parse --show-toplevel' % os.path.dirname(os.path.abspath(__file__))).read().strip()
WORK = os.environ.get('KBAB_WORK', f'{ROOT}/target/kbab')
a = argparse.ArgumentParser(); a.add_argument('base'); a.add_argument('--reps', default=''); a.add_argument('--grades', default='grades.jsonl'); o = a.parse_args()
R = [json.loads(l) for l in open(f'{WORK}/metrics.jsonl')]
if o.reps: lo, hi = map(int, o.reps.split('-')); R = [r for r in R if lo <= r['rep'] <= hi]
G = {}
if os.path.exists(f'{WORK}/{o.grades}'):
    key = json.load(open(f'{WORK}/blind-key.json'))
    for l in open(f'{WORK}/{o.grades}'): g = json.loads(l); G[key[g['key']]] = g
cell = collections.defaultdict(list)
for r in R: cell[(r['variant'], r['task'])].append(r)
ts = sorted({r['task'] for r in R}); vs = [o.base] + sorted({r['variant'] for r in R} - {o.base})
def ratio(v, k, boot=False):
    out = []
    for t in ts:
        x, b = cell[(v, t)], cell[(o.base, t)]
        if not x or not b: continue
        if boot: x = [random.choice(x) for _ in x]; b = [random.choice(b) for _ in b]
        out.append(S.mean(y[k] for y in x) / max(S.mean(y[k] for y in b), 1e-9))
    return S.mean(out)
random.seed(1)
print('| Variant | runs | kb calls (search + get) | vs baseline [95% CI] | weak kb_get | kb KB | tokens vs base | answer score | wrong |')
print('|---|---|---|---|---|---|---|---|---|')
for v in vs:
    rs = [r for t in ts for r in cell[(v, t)]]; bs = sorted(ratio(v, 'kb_calls', True) for _ in range(2000))
    g = [G[r['id']] for r in rs if r['id'] in G]
    sc = f"{S.mean(x['score'] for x in g):.2f} ({len(g)})" if g else '-'; wr = f"{S.mean(x['wrong'] for x in g):.2f}" if g else '-'
    print(f"| {v} | {len(rs)} | {S.mean(r['kb_calls'] for r in rs):.2f} ({S.mean(r['kb_search'] for r in rs):.1f} + {S.mean(r['kb_get'] for r in rs):.1f}) | "
          f"{ratio(v, 'kb_calls'):.2f} [{bs[50]:.2f}, {bs[1949]:.2f}] | {S.mean(r['kb_get_weak'] for r in rs):.2f} | {S.mean(r['kb_bytes'] for r in rs)/1000:.1f} | "
          f"{ratio(v, 'tokens'):.2f} | {sc} | {wr} |")

#!/usr/bin/env python3
"""blind.py [--only v1,v2] [--min-rep K] -> $KBAB_WORK/blind.jsonl (anonymous answers) + blind-key.json, and grade-prompt.md filled in.
Hand grade-prompt.md to a grader subagent; it writes grades.jsonl."""
import json, os, random, argparse
ROOT = os.popen('git -C "%s" rev-parse --show-toplevel' % os.path.dirname(os.path.abspath(__file__))).read().strip()
WORK = os.environ.get('KBAB_WORK', f'{ROOT}/target/kbab'); HERE = os.path.dirname(os.path.abspath(__file__))
a = argparse.ArgumentParser(); a.add_argument('--only', default=''); a.add_argument('--min-rep', type=int, default=0); a.add_argument('--seed', type=int, default=7); o = a.parse_args()
R = [json.loads(l) for l in open(f'{WORK}/metrics.jsonl')]
R = [r for r in R if (not o.only or r['variant'] in o.only.split(',')) and r['rep'] >= o.min_rep]
random.seed(o.seed); random.shuffle(R); key = {}
with open(f'{WORK}/blind.jsonl', 'w') as f:
    for i, r in enumerate(R):
        k = f'k{i:04d}'; key[k] = r['id']; f.write(json.dumps({'key': k, 'task': r['task'], 'answer': r['answer']}) + '\n')
json.dump(key, open(f'{WORK}/blind-key.json', 'w'))
open(f'{WORK}/grade-prompt.md', 'w').write(open(f'{HERE}/grade-prompt.md').read().replace('{WORK}', WORK).replace('{TASKS}', f'{HERE}/tasks.json'))
print(len(R), 'answers ->', f'{WORK}/blind.jsonl; grader prompt: {WORK}/grade-prompt.md')

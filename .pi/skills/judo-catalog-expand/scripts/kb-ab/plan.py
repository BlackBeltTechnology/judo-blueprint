#!/usr/bin/env python3
"""plan.py <base> <variant,...> [--reps N] [--first-rep K] [--seed S] > plan.txt
Interleaved plan: every block (rep x task) holds the baseline and each variant once, shuffled, so drift hits all arms alike."""
import json, os, random, sys, argparse
a = argparse.ArgumentParser(); a.add_argument('base'); a.add_argument('variants'); a.add_argument('--reps', type=int, default=4)
a.add_argument('--first-rep', type=int, default=1); a.add_argument('--seed', type=int, default=1); o = a.parse_args()
tasks = [t['id'] for t in json.load(open(os.path.join(os.path.dirname(__file__), 'tasks.json')))]
random.seed(o.seed)
for r in range(o.first_rep, o.first_rep + o.reps):
    for t in tasks:
        blk = [o.base] + [v for v in o.variants.split(',') if v]; random.shuffle(blk)
        for v in blk: print(v, t, r)

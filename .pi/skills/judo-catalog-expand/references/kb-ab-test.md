# kb structure A/B test

Measures whether a format or file-structure change to `catalog/` makes agents find answers with fewer kb calls. Content never changes. Results so far: `reports/research/kb-structure-ab.md` (2026-11-19 to 11-23; only bold labels as sub-headings won, about 9 % fewer kb calls).

## Setup

| Variable | Default | Set it to |
|---|---|---|
| `KB_CLI` | `kb` on PATH | the kb build the pi sessions load; in a pi-agent-dashboard dev checkout `packages/kb/bin/kb.mjs` (it rebuilds its `dist/` when the source changed) |
| `DASHBOARD_BUS` | found under the global npm roots | pi-dashboard's `.pi/skills/pi-dashboard/scripts/dashboard-bus.ts` |
| `KBAB_MODEL`, `KBAB_THINKING` | `anthropic/claude-sonnet-5-5`, `medium` | the model the build agents use |
| `KBAB_TMP`, `KBAB_WORK` | `/tmp/kbab`, `target/kbab` | scratch kb projects; plans, run list, metrics, grades |

Check first that the pi sessions load the kb version you mean to test (a dev checkout loads `packages/kb-extension/src`; npm installs load the published version).

## Run

```bash
K=.pi/skills/judo-catalog-expand/scripts/kb-ab
$K/make-variant.sh base base
$K/make-variant.sh bold bold                       # one per idea; transforms combine: bold,split
$K/plan.py base bold,split > target/kbab/plan.txt  # 4 tasks x 4 reps per arm, interleaved
xargs -P 6 -L 1 $K/run-session.sh < target/kbab/plan.txt
$K/metrics.py && $K/blind.py                       # then a @review grader on target/kbab/grade-prompt.md
$K/analyze.py base
```

The four tasks (`tasks.json`) each need several catalog sources and carry a grading checklist. A run counts every `kb_*` call, weak `kb_get` (under 200 characters or not found), bytes returned, tokens and seconds; non-kb tool calls must be 0.

## Rules learned the hard way

- **Same-batch baseline only.** The same catalog measured hours apart moved by up to 3 kb calls per task. Never compare against an earlier batch; `plan.py` interleaves the baseline into every block.
- **Noise is about 4 kb calls per run.** 16 runs per arm detect only effects above roughly 10-15 %.
- **Confirm before adopting.** With 8 variants at once, about one false hit at 95 % is expected. The file split looked like 22 % fewer calls in round 1 and showed nothing when rerun. Run the candidate alone against the baseline, decided before looking.
- **Session ids come from the log.** Parallel spawns leak sibling ids into the spawn output; `run-session.sh` tags the prompt and takes the id from the log that holds the tag.
- **Grade blind.** The grader sees only an anonymous key, task and answer. Split large sets between graders at random; they differ in strictness.
- **Static `kb eval` does not tell variants apart.** File-level MRR stayed within ±0.01 for every variant; only live sessions show the effect.
- **Adopting a winner:** the user approves it, the transform runs on `catalog/` (check what it hit: bold navigation links were wrongly converted and restored), a lint rule keeps it, and AGENTS.md names it as a tested exception to add-or-correct.

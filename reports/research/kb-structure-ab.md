# kb structure A/B test (2026-11-19/20)

**Result: no structure-only change gives a reliable kb gain, so none is adopted.** The first round suggested that splitting large agent-docs saves 22 % of kb calls; rerun next to a same-time baseline, the same split saved 3 % and the adopted form 0 %. The difference came from run-to-run noise and drift of the model's behaviour over the hours of testing, not from the structure. The AGENTS.md rule (headings add-or-correct only) and `content-guard` stay as they were.

Data and scripts: [`runs/kbab/`](runs/kbab/) (`summary-table.md`, `results.json`, `metrics.jsonl`, grades, static eval, the harness, and all 165 test sessions as `sessions/<variant>.tar.gz`). The sessions are archived in the dashboard.

## Method

- **Variants:** each a script over a copy of `catalog/` (`variants.py`), placed in `/tmp/kbab/<variant>/` with its own `knowledge_base.json` and a fresh kb index (`make-variant.sh`). The repo was not touched while testing.
- **Static metric:** `kb eval` on the golden (62) and holdout (15) query sets, file level (`static-eval.jsonl`).
- **Live metric:** a new pi session per run (`run-session.sh`), model `anthropic/claude-sonnet-5-5`, thinking medium (the build-test model). The prompt allows only `kb_search` and `kb_get` and asks for a sourced answer to one of four multi-source questions (`tasks.json`: optimistic locking over REST, public actor and guest page, scheduled job plus interceptor failure plus test classpath, attribute rename plus backfill plus schema upgrade). After idle the session is archived.
- **Measured per run** (`metrics.py`, from the session JSONL): kb_search and kb_get calls, weak kb_get (under 200 characters or "not found"), bytes returned by kb, tokens, seconds, other tool calls (always 0).
- **Answer quality:** a blind grader scored every answer against the task checklist (0, 0.5 or 1 per point) and counted wrong statements, seeing only an anonymous key.
- **Harness bug, fixed in the analysis:** with 6 parallel spawns, `run-session.sh` sometimes recorded the id of a sibling session. The variant comes from the session's directory and the task from its prompt, so every run is labelled from its own log; 14 answers graded against the wrong checklist were regraded.

## Variants

| Variant | Change (structure only) |
|---|---|
| V1 emoji | emojis removed; ✅/❌ table cells become Yes/No |
| V2 bold | bold-only lines (`**Usage:**`) become sub-headings |
| V3 generic | generic headings (Overview, Best Practices, …) prefixed with the parent heading; old heading kept as alias |
| V4 hierarchy | one H1 per file, no skipped heading levels (2 files) |
| V5 split | agent-docs over 40 KB (6 files) split into an index plus one part per H2; AGENTS.md not regenerated |
| V6, V7 | V2 + V5; V1 + V2 + V5 |
| V8 adopted | the repo as it would be committed: V5 split plus AGENTS.md rows for every part (kb's dox contract requires a row per file) |
| A2, V5b | a second baseline and the V5 split, rerun interleaved with each other hours later |

## Results

Static eval (file level): all variants within ±0.01 MRR of the baseline (golden 0.789, holdout 0.570); V2 0.800/0.579, V3 0.787/0.561.

Live sessions (16 runs per variant, 4 per task; baseline 17):

| Variant | kb calls | vs baseline, per task | tasks with fewer calls | weak kb_get | tokens (k) | answer score (T1-T3 / T4) |
|---|---|---|---|---|---|---|
| A baseline | 10.4 | 1.00 | | 0.59 | 233 | 1.00 / 0.71 |
| V1 emoji | 9.8 | 0.89 | 3/4 | 0.69 | 215 | 0.99 / 0.67 |
| V2 bold | 9.5 | 0.93 | 3/4 | 0.38 | 200 | 1.00 / 0.88 |
| V3 generic | 9.9 | 0.96 | 2/4 | 0.56 | 218 | 1.00 / 0.62 |
| V4 hierarchy (4 runs) | 10.8 | 1.01 | 2/4 | 0.75 | 210 | 1.00 / 0.83 |
| V5 split | 8.3 | 0.78 | 4/4 | 0.38 | 183 | 0.96 / 0.79 |
| V6 bold + split | 9.2 | 0.87 | 4/4 | 0.50 | 193 | 1.00 / 0.50 |
| V7 bold + split + emoji | 9.0 | 0.83 | 4/4 | 0.38 | 191 | 1.00 / 0.50 |
| V8 adopted | 10.4 | 1.02 | 2/4 | 0.38 | 221 | 1.00 / 0.50 |

Replication, interleaved in one batch:

| Comparison | kb calls vs baseline | tasks with fewer calls | answer score |
|---|---|---|---|
| A2 baseline vs A baseline (same catalog, hours later) | 1.02 | 2/4 | 0.88 vs 0.93 |
| V5b split vs A2 | 0.97 | 3/4 | 0.88 vs 0.88 |
| V8 adopted vs A2 | 1.00 | 2/4 | 0.88 vs 0.88 |

## Why nothing is adopted

- The only large effect (V5, 0.78) did not replicate (V5b 0.97, V8 1.00). The same catalog measured hours apart differs as much as the variants do: A vs A2 per-task means move by up to 3 calls, and on T4 every later run (A2, V5b, V6, V7, V8) misses the rename point that earlier runs found.
- The spread is about 4 kb calls per run, so 16 runs per variant detect only effects above roughly 15 %. No variant shows one when measured next to a same-time baseline.
- Answer quality is equal on T1-T3 (all near 1.0) for every variant.

## For a next test

- Always run each variant interleaved with a same-time baseline in one batch; never compare against an earlier batch.
- Use more runs per cell (8 or more) or more tasks, and a fixed seed or temperature if the provider allows it.
- Record the spawned session id from the spawn response for that call (or spawn sequentially); `run-session.sh` must not take the first id in the output.
- Candidates worth a proper test: kb-side changes are more likely to matter than catalog structure. Rerun this harness on the new kb version against a same-time baseline on the previous one, and try a lower `ranking.laneQuota` in this repo's kb config (no code change).

# kb structure A/B test (2026-11-19/20, rerun 2026-11-23 on the new kb)

**Round 2 result (new kb, see [Round 2](#round-2-new-kb-2026-11-23)): one idea holds up, bold-only lines turned into sub-headings (V2), about 9 % fewer kb calls at equal answer quality, confirmed in a dedicated run. Not yet applied: it is a format change that the add-or-correct rule forbids without approval.**

**Round 1 result: no structure-only change gives a reliable kb gain, so none is adopted.** The first round suggested that splitting large agent-docs saves 22 % of kb calls; rerun next to a same-time baseline, the same split saved 3 % and the adopted form 0 %. The difference came from run-to-run noise and drift of the model's behaviour over the hours of testing, not from the structure. The AGENTS.md rule (headings add-or-correct only) and `content-guard` stay as they were.

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

## Round 2: new kb (2026-11-23)

**Setup changes against round 1:**
- **kb:** the local build of pi-agent-dashboard `develop` (`f735a8282`), which includes `7e2c2d022` (direct-parent chunk links, "section not found" with the section list) and `9bcfbb522` (reindex off the main thread). Test sessions load the kb extension from `packages/kb-extension/src`; all indexes were rebuilt with `packages/kb/bin/kb.mjs`, which rebuilt `dist/` from the current source. Both fixes were checked on the CLI before the run: the `Dashboard Page` hit now has parent `Frontend Extension Points`, and a wrong section returns `(section not found: … — sections:)`.
- **Harness:** each prompt carries a unique `[run kbab-<variant>-<task>-<rep>-<n>]` tag, and the session id is taken from the log that holds the tag. Result: 225 unique ids, 0 mislabelled runs (round 1 had 14). Any `kb_*` tool counts as a kb call (none other than search and get were used).
- **Design:** one batch, all variants interleaved with the baseline (4 runs per task each; the baseline got 4 more at the end, which differed by only 0.5 calls). Answers graded blind, as before.

Data: [`runs/kbab/round2/`](runs/kbab/round2/) (`metrics2.jsonl`, `runs2.txt`, `grades.jsonl`, `blind-keys.json`, `static-eval.jsonl`, `analyze2.py`, and all 225 sessions in `sessions/<variant>.tar.gz`).

Static eval: flat again (golden MRR 0.774–0.778, holdout 0.568–0.579 across variants).

Live sessions, compared with the interleaved baseline runs (kb calls ratio per task, bootstrap 95 % CI):

| Variant | runs | kb calls (search + get) | vs baseline [95% CI] | tasks fewer | weak kb_get | kb KB | tokens vs base | score T1-T3 / T4 | wrong |
|---|---|---|---|---|---|---|---|---|---|
| A-base | 16 | 9.19 (3.3 + 5.9) | 1.00 [0.92, 1.11] | 0/4 | 0.38 | 13.5 | 1.00 | 0.99 / 0.50 | 0.00 |
| V1-emoji | 16 | 8.94 (3.2 + 5.8) | 0.96 [0.88, 1.06] | 3/4 | 0.38 | 13.2 | 0.99 | 0.99 / 0.46 | 0.00 |
| V2-bold | 16 | 8.00 (2.9 + 5.1) | 0.86 [0.77, 0.96] | 3/4 | 0.31 | 11.8 | 0.85 | 0.96 / 0.50 | 0.00 |
| V3-generic | 16 | 9.00 (3.3 + 5.7) | 0.96 [0.87, 1.07] | 2/4 | 0.31 | 14.0 | 0.96 | 0.99 / 0.50 | 0.00 |
| V4-hierarchy | 16 | 8.31 (2.9 + 5.4) | 0.89 [0.80, 1.00] | 3/4 | 0.50 | 12.7 | 0.85 | 1.00 / 0.50 | 0.06 |
| V5-split | 16 | 8.62 (2.9 + 5.7) | 0.91 [0.84, 1.01] | 2/4 | 0.50 | 12.4 | 0.88 | 0.99 / 0.50 | 0.00 |
| V6-bold-split | 16 | 8.31 (3.1 + 5.2) | 0.89 [0.81, 0.98] | 3/4 | 0.25 | 12.9 | 0.84 | 0.93 / 0.50 | 0.00 |
| V7-bold-split-emoji | 16 | 9.00 (3.2 + 5.8) | 0.97 [0.85, 1.11] | 2/4 | 0.50 | 12.6 | 0.92 | 0.97 / 0.50 | 0.12 |
| V8-adopted | 16 | 8.75 (3.1 + 5.6) | 0.93 [0.85, 1.04] | 2/4 | 0.31 | 13.3 | 0.94 | 1.00 / 0.50 | 0.00 |

**Confirmation run** (decided before looking at it, to rule out a lucky pick among 8 variants): V2 against the baseline only, 32 runs each, interleaved.

| Metric | V2 / baseline | 95 % CI |
|---|---|---|
| kb calls | 0.91 | 0.84–0.99 |
| kb_get | 0.90 | 0.82–0.99 |
| kb_search | 0.96 | 0.86–1.08 |
| tokens | 0.92 | 0.84–1.01 |
| kb output bytes | 0.93 | 0.86–1.00 |
| answer score T1-T3 | 0.96 vs 0.97 | equal within one half-point; 0 wrong statements on both sides |

**Reading:**
- **V2 bold → sub-heading** is the only idea below 1 in all three measurements (round 1: 0.93, round 2: 0.86, confirmation: 0.91). The gain comes from fewer `kb_get` calls, mostly on T3 (a question spread over several sections), and does not appear on T4.
- **V6 (bold + split)** is also below 1 (0.89), consistent with it containing V2; the split adds nothing on top.
- **V4 hierarchy** (0.89, CI touches 1.00) affects only 2 files and is not worth a change on its own.
- **Emoji removal, generic heading renames, the split (V5, V8)** stay within the noise, as in round 1.
- **New kb against old kb:** the baselines went from 10.5 to 9.4 kb calls and from 0.61 to 0.41 weak `kb_get` per run. Those runs were days apart, so this is indicative only; it fits the two kb fixes.
- **T4 rename point:** almost no answer in either round states that a CLI rename keeps the `xmi:id`. That is a catalog content gap, not a structure effect; worth checking where agent-docs say it.

**Applying V2** would change bold-only lines (`**Usage:**`) into sub-headings in 67 catalog files. No text is removed and no existing heading changes, but it is a format change for kb, which the AGENTS.md add-or-correct rule excludes; it needs approval first.

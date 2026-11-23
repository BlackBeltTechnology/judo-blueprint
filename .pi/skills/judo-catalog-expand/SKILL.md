---
name: judo-catalog-expand
description: Grow and harden the judo-blueprint catalog with parallel background agents - mine a build session into a validated gap analysis, audit swept projects for compliance, then fix the catalog in ONE edit pass per file (evidence backfill, neutral wording, generic ids and diagram class names), apply verified findings to agent-docs with a reconciled ledger, and mine structure best practices. Use on "apply the findings", "update agent-docs from the review", "mine this build session", "gap analysis", "check projects against the catalog", "backfill evidence", "remove project specific wording", "make blueprints generic", "structure best practices from project X", "run a build test".
---

# judo-catalog-expand

Workflows that grow the catalog beyond single entries (`judo-blueprint-author`). Sweeps and the gate: `judo-catalog-maintain`. Project registry: `.pi/skills/judo-catalog-maintain/references/PROJECTS.md`. Work files: `target/<workflow>/` (git-ignored). This folder is kept out of the kb index on purpose.

## Efficiency rules

1. **Scripts do the deterministic work; agents only judge.** Chunking, merging, dedupe, batching, scope planning, evidence checks, link rewrites and the report are scripts (below). Never hand-write that glue again.
2. **One edit pass per file.** Evidence, wording and renames for a file happen in the same agent turn ([catalog-pass-prompt.md](references/catalog-pass-prompt.md)). Separate passes over the same files caused double edits, steer-and-redo rounds and frontmatter damage.
3. **Settle every rule before spawning.** Ask the user up front: which projects, wording rule, rename map, known-bad project parts. A rule added mid-run costs a full extra pass.
4. **Plan scopes from real counts.** `scripts/scope-split` lists the files that actually match and balances them by size; a blueprint folder always stays with one agent. Guessed counts were off by 3x.
5. **Dedupe before validation.** `gap-report batch` drops duplicates and batches by kind, so validators judge each problem once.
6. **Background, disjoint, no gates in agents.** `Agent(run_in_background: true)`, `@coding` for miners, explorers and editors, `@review` for validators. Agents never edit outside their scope, never run `check-all` or `dox-agents`, never commit.
7. **Short agent answers.** Prompts ask for a 3-line final answer; the detail lives in the agent's JSONL log. Do not relay every late report: compare with what you verified and report only news.
8. **Account for every finding.** A pass is done only when `findings-ledger reconcile` reports 0 unaccounted. Every exclusion (not-platform, rejected, open) is reported to the user with counts from `SUMMARY.md`, never presented as a fact in one line. Never drop findings by a path or source rule: route by content (`findings-ledger route`), and give leftovers to triage agents. Count against the RAW source, not your own inventory: write `raw.jsonl` with one row per raw finding of every source (all kinds: doc, bug, index), so reconcile fails on any row that never reached the inventory or a triage verdict. Triage agents write a verdict for EVERY input line, not only the kept ones.
9. **Content is add-or-correct only.** Agents never rename, reorder or remove headings and never shorten or reword correct text, also not for "format" or "kb" work. `content-guard` (in `check-all`) fails on lost headings and pure deletions. Approved work is applied in the same session, not left in a report.
   One tested format rule applies: a bold-only label line is a sub-heading (see AGENTS.md and `reports/research/kb-structure-ab.md`); `entry-lint` fails on new bold-only label lines.
10. **Verify once, at the end.** `claim-verify` / `vocab-scan` / `rename-ids`, then `dox-agents` and `check-all` (its `kb-eval` catches search regressions).

## Scripts

| Script | Does |
|---|---|
| `session-chunks <s.jsonl> <work>` | Session → round-aligned text chunks (`--prompts` lists rounds, `--dump A B` prints lines) |
| `gap-report batch <work> --gaps GAPS.md` | Merge miners, drop duplicates, list uncovered GAPS refs, write validator batches |
| `claim-verify claims <work> --session S --app APP` | Check every claim's session line, files, commits, catalog target |
| `claim-verify findings <work> <proj>=<src> ...` | Check explore findings' evidence paths and catalog entries |
| `gap-report render <work> --app APP` | Write `GAP-ANALYSIS.md` with checkboxes per distinct item |
| `scope-split <work> <N> --pattern RX` | Balanced, non-overlapping scope files for N agents |
| `rename-ids <logs...>` | Rewrite links, `related:`, `alternatives:` after id renames |
| `vocab-scan` | Project names and client words left in bodies and diagrams |
| `blueprint-scan`, then `blueprint-scan-bm25 25` | After an agent-docs findings pass: match EVERY finding to blueprint and best-practice sections (identifier + BM25); unmatched findings get a recorded `no-blueprint-match` verdict. Check the pairs with `references/blueprint-check-prompt.md` |
| `findings-ledger route <work> <items.jsonl>` | Content-route findings to agent-doc files; leftovers to `triage/unrouted.txt` |
| `findings-ledger plan <work>` | Batches with one writer per file (`batches/`, `file-owners.json`) |
| `findings-ledger wave2 <work>` | Research proposals, triage facts and handoffs → per-owner wave-2 lists |
| `findings-ledger reconcile <work>` | Every finding accounted for; writes `SUMMARY.md` and `OPEN-ITEMS.md`; exit 1 if not |

## 1. Build session → gap analysis

1. Run the build test ([build-test.md](references/build-test.md)) or take an existing builder session.
2. `session-chunks <s.jsonl> target/gap-analysis`; one miner per chunk ([miner-prompt.md](references/miner-prompt.md)).
3. `gap-report batch target/gap-analysis --gaps <APP>/GAPS.md`. Give `uncovered-gaps.txt` to ONE extra miner, then rerun `batch`.
4. One validator per batch ([validator-prompt.md](references/validator-prompt.md)).
5. `claim-verify claims …`, open the "check by hand" lines, `gap-report render …`. The user ticks the file; edit the catalog only for confirmed items (as one catalog pass).

## 2. Compliance explore → one catalog pass

1. One explorer per project ([explore-prompt.md](references/explore-prompt.md)); say which parts of the project are known to be wrong. `claim-verify findings …`; summarise for the user.
2. Agree the pass: projects for evidence, wording rule, rename map (propose generic ids and classes; keep universally generic words like Order, Organization, Invoice).
3. `scope-split target/compliance <N> --pattern '<project>:unrecorded|<project name>|<domain words>'`.
4. One agent per scope file with [catalog-pass-prompt.md](references/catalog-pass-prompt.md), steps E, N and G enabled as agreed.
5. `rename-ids target/compliance/pass-*.jsonl`, `vocab-scan`, `git diff` the frontmatter (agents have renamed projects inside tags), then finish.

## 3. Structure best practices from a project

One agent per area (backend `application/`, frontend `application/frontend-react/`, repository root), writing `catalog/best-practices/<backend|frontend|project>/structure-*.md` in neutral wording from the start, kb-searching existing coverage first. Then run workflow 2's explore on that project: it catches wrong counts and paths.

## 4. Merge project contribution branches

Contributors grow the catalog in `project/<project-id>` branches ([contribute.md](../../../skills/judo-blueprint/references/contribute.md)). `skills/judo-catalog-maintain/scripts/branch-review` lists them; `branch-review project/<id>` writes the classified report and runs `check-all` on the branch merged with `develop`. Judge each change by [merge-criteria.md](../../../skills/judo-catalog-maintain/references/merge-criteria.md); for a large branch, use one `@review` agent per scope from `scope-split --paths` over the branch's changed files. Merge commits or single entries, record what was not merged, and ask the contributor to merge `develop` back.

## 5. Apply findings to agent-docs (reviews, knowledge checks, gap analyses)

Work dir `target/apply-findings/`. About 20 agents for ~400 findings; not one agent per finding.

1. Build `inventory.jsonl` (`id`, `src`, `target`, `text`) from every source: gap analysis, developer answers, judo-ng reviews, doc-gap lists, earlier unverified items. `findings-ledger route` the items without a target file; split `triage/unrouted.txt` (and the uncovered `raw.jsonl` rows) for 2–4 `@coding` triage agents with `references/findings-triage-prompt.md` (a verdict per line in `triage/verdicts-*.jsonl`, kept platform facts in `triage/kept-*.jsonl`).
2. `findings-ledger plan`; one `@research` applier per batch with [findings-apply-prompt.md](references/findings-apply-prompt.md) (quick check, ≤3 lookups).
3. Items left `unverified`: `@research` researchers with [findings-research-prompt.md](references/findings-research-prompt.md) (≤8 lookups, propose text, no edits).
4. `findings-ledger wave2`; one applier per owner batch again (wave 2), so each file still has one writer.
5. One `@review` checker per batch with [findings-check-prompt.md](references/findings-check-prompt.md), after the batch's last wave. Spot-check a few `ok` verdicts yourself against the source.
6. Rewrite the `.agent.md` companions of every changed doc from the corrected text (one `@coding` agent per ~10 files).
7. `findings-ledger reconcile` must pass; report `SUMMARY.md` and send `OPEN-ITEMS.md` to the developers. Then Finish.

## Finish (parent only)

```bash
skills/judo-blueprint-author/scripts/dox-agents
skills/judo-catalog-maintain/scripts/check-all
```

Commit locally by topic; never push to origin.

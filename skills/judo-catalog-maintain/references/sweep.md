---
title: Sweeping a JUDO project into the catalog
description: Operator runbook for a catalog sweep: prepare, overviews, four parallel explorer subagents, merge, cross-validation, authoring, gates and local publishing. Read-only on the project; nothing is pushed.
---

# Sweeping a project

A sweep reads one JUDO project read-only and turns its recurring, hand-written patterns into catalog evidence or new entries. You (the operator's pi session) run it step by step: scripts do the deterministic steps, subagents do the judgement work. `W` is `target/sweep/<project>/<sha7>/` (gitignored; it holds client names and code and is never committed).

**Hard rules.** The project checkout is never modified: the source is a detached worktree at `W/src`. Origin is read-only: nothing pushes, fetches into a remote, or opens a PR. Results reach your branch only by a local `git merge`.

## Sequence

| # | Step | Run | Output | Checkpoint |
|---|---|---|---|---|
| 1 | prepare | `scripts/sweep-prepare <project> [--src DIR] [--sha SHA]` | `W/src` (detached, read-only), `W/bp` (branch `sweep/<project>-<sha7>`), `W/state.json` | Check project, branch and SHA |
| 2 | overview | `scripts/model-overview <project>` then `scripts/custom-overview <project>` | `shape.md`, `domain.md`, `access.md`, `counts.txt`, `custom.md`, `custom.json` | Read the counts; skim `custom.md` |
| 3 | explore | 4 `Agent` calls **in one turn**: `judo-sweep-explore-{model,backend,frontend,schema}`, prompt `Work folder: <abs W>` | `W/lanes/<lane>.json` each | Re-run a weak lane alone; it overwrites only its own file |
| 4 | merge | `scripts/sweep-merge <project>` | `W/candidates.json` | Missing lanes are reported |
| 5 | cross-validate | `Agent judo-sweep-cross-validate`, prompt `Work folder: <abs W>` | `W/decisions.json` | **Approve or edit decisions** before step 6 |
| 6 | author | `Agent judo-sweep-author`, one per batch of about 5 decisions; parallel only for disjoint entries | edits in `W/bp/catalog`, `W/bp/fragments` | |
| 7 | gates | in `W/bp`: `skills/judo-catalog-maintain/scripts/check-all`; write `W/gates.json` `{"result":"pass"}` only when it passes | report | On fail, re-dispatch the author with the report, at most 3 rounds, then stop |
| 8 | publish (local) | `scripts/sweep-publish <project>` | commit on `sweep/<project>-<sha7>`, `W/pr-body.md` (neutral names) | Review, then `git merge sweep/<project>-<sha7>` yourself |
| 9 | record | update the project's `Swept SHA` in `PROJECTS.md` | | |

After several projects: `scripts/sweep-overlap` lists entries that more than one project supports. Their status moves from `single-project` to `emerging` or `established`. When a sweep branch is merged, `scripts/sweep-prepare --clean` removes its worktrees; unmerged ones are kept.

## Reading order for explorers

`shape.md` → `domain.md` → `custom.md` → rationale docs listed in `custom.md` → only then individual source files. In a clean checkout every tracked file under a generator-owned folder is custom (design D10a); file headers are never trusted.

## Roles

Explorers use `@explore` (cheap, wide reading), the cross-validator `@review` (independent second opinion), the author `@coding`. The role map decides the actual models; check it with `list_roles` before a sweep.

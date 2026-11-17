# Merge criteria for project branches

Project branches (`project/<project-id>`) are where the catalog grows. The maintainer merges parts of them into `develop` when they meet these principles. Contributors read the same list to align their changes before pushing. How a contributor works: [contribute.md](../../judo-blueprint/references/contribute.md).

## Hard gates (all must hold, otherwise no merge)

1. **Gates pass** on the branch, merged with current `develop`: `check-all` (entry-lint, spec-check, claim-check, dox-agents, projects, kb-eval).
2. **Scope:** catalog changes touch only `catalog/**` and the project's own row in `PROJECTS.md`. Changes to `skills/`, `.pi/`, `tests/` or CI are a separate review, never merged with catalog content.
3. **Platform truth:** a new or changed platform claim in `agent-docs/` or an entry has evidence (judo-ng `repo@sha:path:line`, or a reproducible check), or says *verify*. An entry never contradicts `agent-docs`.
4. **Generic:** no project names, client business words or single-project facts in bodies. Project only in `projects:`, `evidence:`, `project:` tags.
5. **Real evidence:** the contributing project's evidence is a path that exists in its repository (at the swept or stated SHA), not `unrecorded`.
6. **No model files:** structure diagrams are plain Mermaid; no `.model` file is added anywhere in the repo.
7. **No loss:** a change does not delete another project's citation, variation or entry unless it is shown wrong, with evidence.

## Principles for judging content

| Change | Merge when | Otherwise |
|---|---|---|
| New entry | The mechanism is reusable beyond the project and not already covered (kb search by the reviewer finds no duplicate) | Fold it into the covering entry as a variation; or keep it in the branch |
| Project added to an existing entry | Evidence path shows the same mechanism | Keep in branch until evidence exists |
| Different method for the same problem | Added as `## Variations` or a new entry with mutual `alternatives:`; *When to use / avoid* says how to choose | Never as a replacement of the existing method |
| Correction of an entry or agent-doc | Evidence shows the old text is wrong | Ask the contributor; mark *verify* |
| New project row in `PROJECTS.md` | URL and branch are real | Maintainer sets the weight on merge |

**Status follows usage:** each project that cites an entry with real evidence counts; 1 project `single-project`, 2 to 3 `emerging`, 4 or more `established`. Entries become stronger as more project branches add their evidence; nothing else upgrades status.

**Two branches change the same entry:** keep both projects' evidence; merge different methods as variations. When the two claims contradict, the one backed by agent-docs or judo-ng evidence wins; the other is noted under *When to avoid* or dropped with a reason in the merge commit.

## How the maintainer merges

```bash
skills/judo-catalog-maintain/scripts/branch-review                  # all project/* branches ahead of develop
skills/judo-catalog-maintain/scripts/branch-review project/<id>     # one branch: classified diff + gate run
```

`branch-review` writes `target/branch-review/<branch>.md`: commits, changed files by kind (new entry, entry changed, agent-docs, PROJECTS.md, out of scope), hard-gate violations it can detect, and the `check-all` result on the branch merged with `develop` in a temporary worktree.

- Merge whole commits that pass (`git cherry-pick` or a merge commit), or single entries (`git checkout project/<id> -- <paths>`, then gates, commit `merge(<id>): <what>`).
- Record what was not merged and why in the merge commit body, so the contributor can fix it in their branch.
- After merging, `dox-agents` and `check-all` on `develop`, then tell the contributor to merge `develop` back into their branch.

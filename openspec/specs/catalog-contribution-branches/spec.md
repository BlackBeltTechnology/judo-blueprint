# catalog-contribution-branches Specification

## Purpose
The catalog grows from use. Each JUDO project contributes on its own branch of this repository, its own kb reads that branch, and the maintainer merges what meets published criteria into `develop`, from which new projects branch. This replaces a separate contributor-consent record: pushing to a project branch is the contribution.

## Requirements

### Requirement: One contribution branch per project
Each contributing JUDO project SHALL work on a branch `project/<project-id>` of this repository, created from `develop`. `<project-id>` is the project's lowercase repository name. Short-lived topic branches `project/<project-id>-<topic>` merge into the project branch. Contributors SHALL NOT push to `develop`, `master` or tags.

#### Scenario: New project starts
- **WHEN** a new JUDO project wants to contribute
- **THEN** it branches `project/<project-id>` from the current `develop`, adds its row to `PROJECTS.md` in that branch, and pushes the branch

#### Scenario: Protected branches
- **WHEN** a contributor pushes
- **THEN** only a `project/*` branch is updated; `develop`, `master` and tags are unchanged

### Requirement: Project kb reads its own branch
`judo-blueprint/scripts/pin-source --branch project/<project-id>` SHALL write a git kb source for that branch with `subdir: catalog` into the project's `knowledge_base.json`. It SHALL accept only `project/*` branches for `--branch`, and reject `develop`, `master`, `main`, `HEAD` and `project/*` given as a tag. Consumers that do not contribute pin a release tag as before.

#### Scenario: Contributor setup
- **WHEN** `pin-source --branch project/alpha --project <app>` runs
- **THEN** `<app>/.pi/dashboard/knowledge_base.json` has one judo-blueprint git source with `pin: project/alpha` and `subdir: catalog`, and earlier judo-blueprint sources are replaced

#### Scenario: Re-index after a push
- **WHEN** the contributor pushes new catalog content to `project/alpha`
- **THEN** `kb index` (or a pi reload) in the app makes the new content searchable through `kb_search`

### Requirement: Contributors align with the catalog's methods
The contribution guide (`judo-blueprint/references/contribute.md`) SHALL tell contributors how to add what is missing in their branch: platform facts with evidence or *verify*; new entries through `judo-blueprint-author`; their project's evidence on existing entries; a different method as a variation or alternative rather than a replacement; generic wording. Contributors run `check-all` before pushing.

#### Scenario: Different method
- **WHEN** a project solves a covered problem differently
- **THEN** the branch adds the method under `## Variations` or as a new entry with mutual `alternatives:`, and the existing method stays

### Requirement: Published merge criteria
`judo-catalog-maintain/references/merge-criteria.md` SHALL list the hard gates (check-all on branch plus develop, catalog-only scope, platform evidence or *verify*, generic wording, real evidence paths, no model files, no loss of other projects' citations) and the principles for new entries, added evidence, differing methods, corrections, conflicting branches and status. Contributors and the maintainer use the same document.

#### Scenario: Out-of-scope change
- **WHEN** a project branch changes `skills/`, `.pi/`, `tests/` or CI
- **THEN** that change is reviewed separately and never merged together with catalog content

#### Scenario: Status grows with usage
- **WHEN** a third project branch adds real evidence to an entry and it is merged
- **THEN** the entry's status becomes `emerging` (2 to 3 projects), and `established` at 4 or more

### Requirement: Branch review tool
`judo-catalog-maintain/scripts/branch-review` SHALL list `project/*` branches with commits ahead of and behind `develop`, and for one branch write `target/branch-review/<branch>.md`: commits, changed files by kind, detectable hard-gate violations (out-of-scope paths, deleted entry files, added `unrecorded` evidence, changed citation lines, merge conflict) and the `check-all` result on the branch merged with `develop` in a temporary worktree. It SHALL never push or modify `develop` or the branch.

#### Scenario: Review a branch
- **WHEN** the maintainer runs `branch-review project/alpha`
- **THEN** the report exists, the repository's branches are unchanged, and the exit code is 1 if any violation or gate failure was found

#### Scenario: Merge and sync back
- **WHEN** the maintainer merges accepted commits or entries into `develop`
- **THEN** the merge commit records what was not merged and why, and the contributor merges `develop` back into the project branch

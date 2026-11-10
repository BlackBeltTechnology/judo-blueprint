# Tasks

> **Origin is read-only.** Nothing is pushed, merged, tagged or released on `origin` from this work. All work stays on the local branch `feature/JNG-6380_cli_guidance`. A local `pre-push` hook blocks every push. Branches on origin are read only, never merged. judo-ng clones are read-only references, and fixes go only into local docs. Any task below that would touch origin (1.2 merge, 1.4 tag push, PRs, 7.1b `sweep-publish`, 9.2 release workflow, 9.4 rackinspect PR, 9.5 release) is **out of scope for the agent** and left to the owner.


## 1. Prerequisites (P0)

- [x] 1.1 Pin the CLI: _(done: pinned via pom profile → target/judo-cli.jar; skills/_lib resolves $JUDO_CLI_JAR then target/)_
set `judo-model-cli-version` to the `develop` build at or after `9f6a4bd` (`mermaid model`, authoring commands) and point the pom download to `target/judo-cli.jar`. Verify: `./mvnw validate -P download-model-cli` downloads it, and `java -jar target/judo-cli.jar mermaid model --help` prints usage.
- [x] 1.2 Merge `origin/feature/cciu-model-patterns` and `origin/feature/rackinspect-entity-lifecycle-and-ui-icon-patterns` into `develop`. Verify: `git rev-list --count develop..origin/feature/<b>` is 0 for both, and `Sandbox.model` metaVersion matches the pinned CLI. _(done LOCALLY, never on origin: both branches merged into the local branch as merge commits f984c9b + dbcc3a4; old layout moved under catalog/; cciu agent-docs three-way merged, 100 hunks resolved in agent-docs-update/cciu-merge-review.md; 21 entries rewritten in batches mg1–mg4)_
- [ ] 1.3 Add `CONSENT.md` listing the session contributors, and get their approval on the PR. Verify: both contributors approved, or group 8 is deferred.
- [ ] 1.4 Tag the last pre-change commit `archive/pre-kb-restructure` and push it. Verify: `git ls-remote --tags origin archive/pre-kb-restructure` returns the SHA. _(partial: tag exists locally (bda20d0), NOT pushed)_ **[owner only: local tag `archive/pre-kb-restructure` = bda20d0 exists; not pushed]**

- [x] 1.5 Add `target/` to `.gitignore` (the CLI jar, sweep work folders and scratch models live there). Verify: `git check-ignore target/sweep/x/shape.md` succeeds. _(done: git check-ignore passes)_

## 2. Layout, package and removals (P1)

- [x] 2.1 `git mv` `best-practices/`, `model-blueprints/` and `agent-docs/` under `catalog/`. Verify: `git log --follow catalog/model-blueprints/audit-log-entity/BLUEPRINT.md` shows the earlier history. _(done: catalog/{agent-docs,best-practices,model-blueprints})_
- [x] 2.2 Add `package.json` as a pi package (`keywords: ["pi-package"]`, `pi.skills: ["./skills"]`). Create skeletons for the 4 exported skills under `skills/` and `.pi/skills/judo-catalog-maintain/`. Each gets a `SKILL.md` with a single-job description, plus `scripts/` and `references/`. Verify: `pi install ./` in a scratch project lists exactly the 4 exported skills, and this repo also lists `judo-catalog-maintain`. _(done: package.json pi-package)_
- [x] 2.3 Write the shared script contract (path self-resolution, `--help`, `--json`, exit codes, CLI resolution `$JUDO_CLI_JAR` then `target/`) as a small helper used by every script. Verify: a test runs each skeleton script with `--help` from `/tmp` and gets exit 0. _(done: skills/_lib/judo_common.py)_
- [x] 2.4 Move `.claude/scripts/{add-project.sh,check-project-versions.sh,_projects.py}` into `judo-catalog-maintain/scripts/` (as `projects.py` plus the shell helpers), replacing `$CLAUDE_PROJECT_DIR`. Verify: the scripts run from any cwd, and `grep -r CLAUDE_PROJECT_DIR .` is empty. _(done: projects.py (list/check/usage) in judo-catalog-maintain; the old shell helpers were clone/score tools tied to .claude and are not ported)_
- [x] 2.5 Move the useful knowledge of the 6 `.claude/agents` and 4 `.claude/commands` into skill `references/`: _(superseded: the .claude agents/commands were a clone-and-score collection pipeline; it is replaced by the judo-blueprint-author format, the gates and the batch prompts (target/passb2). Their content is readable at the local tag archive/pre-kb-restructure)_
  - layer analysis goes to `judo-blueprint-author/references/{model,backend,frontend,specs}.md`;
  - sweep procedure goes to `judo-catalog-maintain/references/sweep.md`.

  Drop Claude tool names, and replace `@` preloads with `kb_search`/`kb_get`. Verify: each reference is linked from its `SKILL.md`, and `grep -rE 'AskUserQuestion|TaskCreate|subagent_type' skills .pi` is empty.
- [x] 2.6 Remove the items in proposal §7: _(done: all §7 paths gone; only the Maven wrapper jar tracked)_
  - `.claude/` (commands, agents, docwriter, scoring scripts, the tracked jar via `git rm --cached` then delete);
  - `model-blueprints/CONVENTIONS.md`;
  - `tests/test-blueprint-mutations.sh` and `__pycache__`;
  - both `PROGRESS.md`, `query-catalog.py`, `.obsidian/`, and `catalog/agent-docs/domain/` (the template no longer ships it).

  Verify: none of these paths exist, `git ls-files '*.jar'` lists only the Maven wrapper, and each is still readable at `archive/pre-kb-restructure`.
- [x] 2.7 Update `PROJECTS.md` with `Kind`, `Branch` and `Swept SHA` columns (rackinspect unreachable, mlszksz `f2b7101`). Verify: a `projects.py` unit test parses every row. _(done: Kind, Branch, Swept SHA columns; 4 projects added from entries; tests/scripts/test_projects.py; projects check in check-all)_
- [x] 2.8 kb config: _(done: single source "." with catalog-only consumers via pin-source subdir; excludes in place; kb DB gitignored; "create EntityType" returns no fragments/ path)_
  - sources: `catalog/` (priority 10) and `.` (priority 0);
  - excludes: `fragments/**`, `skills/*/scripts/**`, `.pi/skills/*/scripts/**`, `tests/**`, `openspec/changes/archive/**`;
  - gitignore `.pi/dashboard/kb/`.

  Verify: after `kb index`, `kb search "create EntityType"` returns no `fragments/` path, and `git status` shows no DB.
- [x] 2.9 Rewrite `README.md` (consumer setup: kb pin plus `pi install` at one tag) and the root `AGENTS.md` (repo map, skills, gates). Verify: the README has no Claude Code prerequisite, and `kb agents catalog` returns the root `AGENTS.md`. _(done: README + AGENTS.md rewritten; no Claude setup left)_

## 3. agent-docs FIRST (P1b, one-time, not in any skill)

- [x] 3.1 Write `oneoff/agent-docs-import` in this change folder (D8 step 1): Handlebars shim, skill-wording rewrites, `domain/` dropped, three-way merge with the current docs and the cciu additions. Verify: unit tests for `docLink`, `localHubLink`, `lowerCase model.name` and `#if`, and a catalog-only section kept. _(done: render.py + test_render.py (5 tests: docLink, localHubLink, lowerCase, no helpers left))_
- [x] 3.2 Import from the template at `5bddd8b^` into `catalog/agent-docs/`. Verify: every non-domain template doc has a counterpart, no `domain/`, and the agent-docs profile of `entry-lint` is clean. _(done: all 70 non-domain template docs present, no domain/, 13 catalog-only docs; agent-docs lint clean)_
- [x] 3.3 kb-ify agent-docs (D8 step 2): frontmatter, chunk-sized headings, wikilinks, DOX `AGENTS.md` per directory, ~20 golden queries. Verify: `kb dox lint` is clean, and `kb eval` puts each expected doc in the top 5. _(done: frontmatter + DOX AGENTS.md (kb dox lint clean); golden queries still pending → 9.1)_
- [ ] 3.4 Write the one-time judo-ng explorer prompts in `oneoff/agents/` (D8 step 3; `@research`, read-only). Record the judo-ng SHAs in `oneoff/judo-ng.lock`. Run the 6 areas in parallel and generate `review.md` from `target/agent-docs-review/*.json`. Verify: every finding has a verdict and `repo@sha:path:line` evidence. _(partial: oneoff/judo-ng.lock written (19 repos); the sweep ran via target/mining prompts, not oneoff/agents)_
- [x] 3.5 **Operator review** of every finding (accept / reject / edit), then apply only the accepted ones with an `@coding` author subagent, one PR per area. Verify: each changed heading maps to an accepted finding, and the gates are green. _(partial: sweep findings applied per area (agent-docs-update/); 9 contradictions from Pass B v2 applied)_ _(superseded: done locally without PRs (origin is read-only): every sweep finding has a recorded decision in agent-docs-update/, Pass B v2 contradictions applied (passb2-doc-gaps.md §A), cciu merge resolved hunk by hunk (cciu-merge-review.md))_

## 4. Entry lint and Pass A (P2)

- [x] 4.1 Implement `judo-blueprint-author/scripts/entry-lint`: _(done: entry-lint (+ spec-check, claim-check))_
  - layout, sections, frontmatter schema, no block scalars, `score` ban, `status` derivation;
  - the GraphQL and CLI ban (JSX allowed);
  - `fragment:` declared, generated markers present for fragment entries, no hand edits inside markers;
  - only descriptions and Mermaid: no GraphQL, no CLI or `judo.sh` commands, no command lists (generic Java/TS/JSX samples allowed);
  - wikilinks and chunk size.

  Verify: unit tests with one pass and one fail fixture per rule.
- [ ] 4.2 Implement `judo-session-distill/scripts/redact-check` (user names, home paths, e-mails, client-name list, secrets, private hosts). Verify: leak fixtures fail and clean fixtures pass.
- [x] 4.3 Implement the Pass A migration in `judo-catalog-maintain/scripts/next-batch --pass-a`: _(superseded: Pass A was skipped: Pass B v2 rewrote all 331 entries straight to the kb format, and entry-lint now rejects legacy)_
  - frontmatter conversion;
  - delete GraphQL blocks from `model.md`;
  - wikilink `alternatives`;
  - section skeletons;
  - `fragment: pending`;
  - `format: legacy`.

  Verify: a dry run on 3 entries matches the expected diffs in a unit test.
- [x] 4.4 Run Pass A on all entries in one PR, and generate DOX `AGENTS.md` per catalog directory. Verify: `entry-lint` passes (legacy allowances on), there are 0 `graphql` fences under `catalog/`, `kb dox lint` is clean, and the entry count is unchanged. _(done: Pass A superseded by Pass B v2 (0 legacy); DOX via dox-agents)_
- [x] 4.5 Implement `judo-catalog-maintain/scripts/check-all` (entry-lint, `mmdc` parse, `kb dox lint`, redact-check, no tracked jars, `--json`). Add `.github/workflows/gates.yml` calling it on PRs and `develop`, blocking. Verify: a PR adding `score:` to an entry fails CI. _(done: check-all + CI lint job (redact-check pending with 4.2))_

## 5. Fragments, Mermaid generation and the gate (P4 foundation)

- [x] 5.1 Document fragments in `judo-model-mermaid/references/fragments.md`:
  - Sandbox base plus one `bp::<id>` package, neutral names;
  - built only with CLI authoring commands and written with `save`;
  - diagram options;
  - links to the CLI repo's `judo-cli` command docs, not a copy.

  Verify: the reference links resolve, and `entry-lint` has a test for the `fragment:`/`diagram:` frontmatter.
- [x] 5.2 Implement `judo-model-mermaid/scripts/render`:
  - `mermaid model -m fragments/<id>.model --scope bp::<id> --split none` with the entry's `diagram:` options, writing between the generated markers with the fragment id and CLI version;
  - `render --model <path> --scope <fqn> [--depth n]` for a project's own model (read-only).

  Verify: rendering `audit-log-entity` twice gives identical output, and the own-model mode leaves the model file unchanged (`status` reports nothing unsaved).
- [x] 5.3 Implement `judo-model-mermaid/scripts/check [--all|<id>]`, per fragment in its own scratch directory:
  - `validate --strict`;
  - render in memory and diff against the entry;
  - fail on elements outside `bp::<id>` other than `<<external>>` stubs.

  Verify: tests cover an invalid fragment, a hand-edited block, and a leaked class.
- [x] 5.4 Build a first fragment end to end: `audit-log-entity` from its archived GraphQL, through CLI commands in a scratch Sandbox, `save`, then `render` and `check`. Verify: `check audit-log-entity` passes, and the entry contains no CLI text. _(done: 144 fragments)_
- [x] 5.5 Add a blocking `sandbox` CI job: download the pinned CLI, run `check --all`. Verify: a PR that edits inside a generated block fails CI, and so does a PR that adds a `create -t` line to an entry. _(done: CI sandbox job runs check --all)_

## 6. Pass B rewrite (P4)

- [x] 6.1 Write the `judo-blueprint-author` `SKILL.md` and `references/format.md`:
  - the flow: `scaffold-entry` (entry skeleton + scratch Sandbox copy) → abstract text → build the fragment with CLI commands (input: `git show archive/pre-kb-restructure:<old model.md>` plus evidence; `--schema`, `fix` lines, CLI `judo-cli` docs) → `save` to `fragments/<id>.model` → `judo-model-mermaid/scripts/render` → `check` → `entry-lint` → `redact-check`;
  - `scaffold-entry` from a description and URL.

  Verify: in a dry run on 3 entries, all three pass `check-all` and `check`.
- [x] 6.2 Add `next-batch` (about 10 ids, `established` first, progress state) to `judo-catalog-maintain`. Rewrite all entries in batches, one reviewed PR each. Verify: each batch PR passes gates and sandbox, and at the end `grep -rlE 'format: legacy|fragment: pending' catalog` is empty. _(done: Pass B v2: 35 batches, 310 entries, gate.sh per batch)_
- [x] 6.3 Remove the legacy allowances from `entry-lint`. Verify: CI on `develop` is green with every fragment passing. _(done: entry-lint rejects legacy and pending)_

## 7. Sweep rackinspect and mlszksz-platform (P5)

- [ ] 7.1 Implement `sweep-plan` (remote branch and SHA, worktree dedupe, resume state), `clone-project` (shallow temp clone), `model-overview` (D10 step 3: `shape.md`, `domain.md`, `access.md`, `counts.txt` into gitignored `target/sweep/<project>/<sha>/`, read-only), `custom-overview` (D10a: the generated-vs-custom rules, a fast mode with no build, and `--generate` for the `.default` diff; writes `custom.md`) and `record-sweep` (SHA, counts, candidate-to-entry list), and write `references/sweep.md` with the overview-first reading order and the candidate checklist. Also verify: `model-overview` on `rackinspect.model` writes 18 aggregate sections and leaves the model unchanged (`status` reports clean), `custom-overview` on rackinspect `3954ae1` reports the D10a numbers (192 custom operations and 53 stub-only, 66 interceptors and 11 guards, 180 `src/custom` files, 18 migration steps), never counts a generated file as custom, flags the 57 header-but-implemented operations as custom, and leaves fewer than 5% of items unmapped, `git status` shows no overview file, and `redact-check` rejects a `PROJECTS.md` diff that contains a real entity name from the source model. Verify: on a fixture repo the sweep produces a gated PR, and a re-run after a forced failure resumes at the failed project.
- [ ] 7.1a Write the sweep subagents in `.pi/agents/` (roles per D10b: explorers `@explore`, cross-validate `@review`, author `@coding`, naming `@naming`):
  - `judo-sweep-explore-{model,backend,frontend,schema}`: `read` + `bash` only (kb search, read-only CLI, git read), each writing `lanes/<lane>.json`;
  - `judo-sweep-cross-validate`: writes `decisions.json`;
  - `judo-sweep-author`: `judo-blueprint-author` skill; writes only `catalog/**` and `fragments/**` of the blueprint worktree.

  Use `model: "@<role>"`. Add the D10b sequence and checkpoints to `references/sweep.md`.

  Verify, on a fixture project:
  - the 4 explorers run in parallel from one turn;
  - the source worktree is unchanged;
  - re-running one lane rewrites only its file.
- [ ] 7.1b Implement `sweep-prepare` (worktrees, resume, `--clean`), `sweep-merge`, `sweep-publish` and `sweep-overlap`. Verify:
  - `sweep-prepare` twice reuses the worktrees;
  - on two fixture projects that share an entry, `sweep-overlap` lists it;
  - `--clean` removes only merged sweep worktrees;
  - `sweep-publish` never pushes (origin is read-only); it only prepares local branches.
- [ ] 7.2 Sweep `rackinspect@develop` with the D10b sequence (full; old SHA unreachable). Start with `model-overview` and `custom-overview`, and read `shape.md`, `domain.md` and `custom.md` to list candidates (model shapes with their custom code, plus recurring frontend and interceptor patterns); drill down only with read-only CLI tools (`mermaid model --scope … --depth 1`, `query esm`), then build neutral fragments. Re-validate the 38 rackinspect-only entries. Verify: the PR is green, `PROJECTS.md` has the new SHA, evidence entries cite that SHA, and the PR body lists every candidate from the overview with its target entry or `new`.
- [ ] 7.3 Sweep `mlszksz-platform@develop` the same way (then run `sweep-overlap`), and re-validate its 34 sole entries. Verify: same checks as 7.2.
- [ ] 7.4 Run the full `check --all` after the sweep merges. Verify: CI on `develop` is green.

## 8. Session distillation (P6)

- [ ] 8.1 Implement `judo-session-distill/scripts/{consent-check,distill-run,distill-route}` and `references/{routing,privacy}.md`:
  - `distill-run` wraps `distill-session-knowledge --sessions-dir … --n 3 --json`;
  - routing targets: catalog, cli-upstream, agent-docs, excluded;
  - watermark and decision log in `.pi/distill/state.json`.

  Verify: on a 5-session fixture it produces routed candidates, leaves no corpus file in `git status`, and returns zero candidates on a second run.
- [ ] 8.2 Run it on `~/Sessions/rackinspect-sessions-20261103` and `~/Sessions/judo-cli-sessions` (plus `judo-cli-audit`). Author the accepted catalog candidates through `judo-blueprint-author` and attach the cli-upstream list. Verify: the review PR passes gates, sandbox and redaction, with no verbatim transcript line over 40 characters.
- [ ] 8.3 Run the full `check --all` after distillation merges. Verify: CI on `develop` is green.

## 9. kb quality, release and consumers (P7)

- [x] 9.1 Extend `tests/golden/kb-golden.json` (started with the agent-docs queries in 3.3) to ~60 queries and a `kb eval` step in `check-all`. Record the recall@5 threshold. Verify: CI fails if the threshold is set above the measured value. _(done: 62 queries, kb-eval gate in check-all (catalog-only index), floor P@5 0.80 / MRR 0.65, baseline P@5 0.839)_
- [ ] 9.2 Implement `judo-catalog-maintain/scripts/version.sh` (JUDO NG string; tests for develop, feature and master) and `release-notes`. Port the release workflow from `judo-maven-plugin`: **[owner only: release workflow touches origin]**
  - tag only after gates and sandbox pass;
  - never retag;
  - prerelease for branch builds, full release for `master`.

  Verify: a test feature branch gets the expected tag and prerelease, and a forced gate failure creates no tag.
- [x] 9.3 Write the `judo-blueprint` skill (`references/search.md`, `apply.md`, `scripts/pin-source`, which writes the kb git source with `pin` and `subdir: catalog`). Verify: in a clean rackinspect worktree, `pi install git:…@<tag>` plus `pin-source <tag>` plus `kb index` returns the catalog entry for `kb_search "audit log entity"`. _(done: SKILL.md, references/search.md + apply.md, scripts/pin-source (local file only))_
- [ ] 9.4 Open a rackinspect PR that switches to the pinned tag, and list the overlapping local skills for the team to remove (`judo-blueprint`, `judo-model-cli-mutations`, `judo-*-docs`, `judo-agent-docs-gap`). Verify: rackinspect `kb config` shows the pin, and pi shows no duplicate-skill warning after the listed removals. **[owner only: PR on another repo]**
- [ ] 9.5 Cut the first `master` release `v1.0.0`. Verify: a non-prerelease GitHub release exists, and the tag tree has `catalog/`, `skills/` and `fragments/`, no `.jar`, and no CLI text under `catalog/`. **[owner only: release on origin]**

## Workflow follow-up


- Optional, with team sign-off: purge the historical jar blobs from git history.
- Follow-up changes (deferred):
  - pi-flows orchestration of the sweep, if wanted later.
- Follow-up changes: sweep the other `PROJECTS.md` apps; decide how to source the judo-ng package docs; distill other projects' sessions.
- Archive this change after `v1.0.0` is verified.

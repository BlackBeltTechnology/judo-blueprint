# Catalog update research log

Everything used to update the catalog: sources, analyses, agent outputs, ledgers and decisions. Not indexed by kb (consumers index only `catalog/`). Add a section for every new pass; never delete earlier ones.

## Contents

| Path | What |
|---|---|
| `runs/apply-findings/` | judo-ng read findings (2,864) + knowledge-check + build-test findings: inventory, `raw.jsonl`, triage verdicts, batches, apply ledgers, checker verdicts, `SUMMARY.md`, `OPEN-ITEMS.md` |
| `runs/apply-findings-r16/` | webshop review round R16 (9 catalog issues) |
| `runs/bp-check/` | 3,109 findings checked against model blueprints and best practices |
| `runs/apply-findings-webshop/` | webshop build-test gaps R16–R19 (74 findings incl. R19-12..17), `r19b/` agent outputs of the last pass |
| `runs/open-verify/`, `runs/open-verify2/` | verification of the 106 open items from judo-ng code, and the settle pass of the last 22 |
| `judo-ng-read/` | the full judo-ng read: `findings.md`, reader/validator prompts, `review.md`, worktree update log (`wt-update.log`, latest `develop`), `judo-ng.lock`, `manifest.json` |
| `webshop-run/` | the complete webshop build-test sessions (`*.jsonl.gz`, unmodified pi session logs; raw `.jsonl` kept locally, git-ignored), `GAPS.md` at the time of copy, orchestration log |
| `../judo-ng-issues/` | issues for the judo-ng developers derived from this research: `CLI.md`, `FRAMEWORK.md` |

Every ledger reconciles with `.pi/skills/judo-catalog-expand/scripts/findings-ledger reconcile runs/<work>` (0 unaccounted, 0 open).

## Passes and results

| Date | Pass | Input | Result | Commit |
|---|---|---|---|---|
| 11-17 | Apply verified findings | judo-ng read, knowledge check, build test | agent-docs facts, kb frontmatter and companions | `272b6fc` |
| 11-17 | Triage all judo-ng findings against the raw source | 2,864 rows (1,332 doc, 1,192 bug, 249 index, ...) | 113 more platform facts applied and double-checked; 206 index rows not platform | `64e60e4` |
| 11-17 | Webshop review round | R16-C2..C10 | 9 fixes | `9afde20`, `7a4d613` |
| 11-17 | Blueprint / best-practice check | 3,109 findings | fixes in blueprints and practices | `d8fe456` |
| 11-19 | Transformation mode default | judo-ng code | ZETA for the ESM workflow, ETL in the JSL plugin | `b177f13` |
| 11-19 | Webshop gaps R16–R19 | 68 gaps | 23 platform facts applied and double-checked | `377bfa1` |
| 11-19 | Open items from judo-ng (latest develop, CLI pin bumped) | 106 | 41 fixes, 22 already correct, 12 rejected, 9 not platform, 22 left | `8d3ce43` |
| 11-19 | Settle the 22 left (no open status allowed) | 22 | 17 fixes, 3 already correct, 2 rejected | `133e736` |
| 11-19 | Webshop gaps R19-12..17 | 6 gaps, 18 sub-claims | 10 applied, 5 already correct, 4 rejected; checker fixed 1 citation | `c577545`, `b054a6b` |

## 2026-11-19: webshop gaps R19-12..17

Agent outputs: `runs/apply-findings-webshop/r19b/out-1.jsonl`, `out-2.jsonl`; ledger `ledger/zzzz-r19b.jsonl`; checker `check/zzzz-r19b.jsonl`.

### Duplicate type imports (R16-1, R19-12, R19-13, R19-15, R19-17)

- **Observed:** `./judo.sh build -i` fails in the admin frontend at `pnpm run format`: `import type { CsvFile, CsvFile, ... }`.
- **First reproduction (rejected as evidence):** `judo-cli transform` UI model + React generator: no duplicates in any order. Not the failing pipeline.
- **Controlled reproduction (the app's own Maven pipeline, `mvn -o` frontend-react/model then admin generate-sources, git worktrees):**

  | Worktree | Actor order | Admin files with duplicate imports |
  |---|---|---|
  | e7aa555 | Customer, Admin, Guest | 48 (12 pages) |
  | e7aa555, Guest moved first | Guest, Customer, Admin | 0 |
  | eea170d | Guest, Customer, Admin | 0 |
  | 980b1a6 | Customer, Admin (shared output TO) | 0 |

- **Cause:** `Esm2UiZetaTransformation.java:1720-1723` (one pass per actor, file order, shared UI model); `fixCallOperationActionDefinitions` `:835-907` rebinds call-operation actions of all actors to the current actor's same-named operation (`findContainerClassType` `:1182-1197`, `setOperation` `:907`); `UiPageHelper.java:154` `HashSet<ClassType>` (identity), `:181` adds the rebound output class. 126 cross-actor references in the failing model, 54 with the actor first.
- **R19-13 (two actors, shared output TO) rejected:** not reproduced at 980b1a6. The failing build ran right after a branch switch, after two failed `generate` runs (hand-edited `frontend-react/README.adoc`): stale model.
- **Catalog:** `agent-docs/deployment/build-process.md` known issue (cause, workaround scoped to the tested model, stale-model caveat); `best-practices/frontend/dual-actor-frontend-architecture.md`.

### Other R19 claims

| Claim | Result | Evidence |
|---|---|---|
| `anonymous` default | `true`; actor without the flag and principal is public | `esm.ecore:434-436`, `KeycloakLoginInterceptor.java:138-139`, CLI query |
| `managed` on anonymous actor | refused, stored `true` | `EsmFieldRules.java:425-428`, CLI |
| `judo.sh build -M -B` | stops and deletes Karaf, builds only frontend | `judo.sh.hbs:837-851` |
| `supportGuestAccess` | only on non-anonymous actors | `EsmFieldRules.java:426-427`, `Auth.tsx.hbs:7` |
| Base URL `/` | static `web-root/index.html`, override via `.generator-ignore` | template `web-root/.../index.html:11` |
| List access path | `/api/<Model>/<Actor>/<Actor>/<access>/~list` | `OperationHelper.java:118-120` |
| First load `Hello!` | `ComponentProxy` fallback until services are ready | `pages/index.tsx.hbs:427-431` |
| generate does not add a new actor module to the poms (R19-17 a) | rejected: it does | scratch `generate-sources` |
| generate overwrites `src/custom` of a new actor (R19-17 c) | rejected: generate writes no `src/custom` | scratch generate |
| CLI failed-script recovery | save + `discard --force` (EMF command stack) | `EsmTransaction.java:85-86`, `SaveCommand.java:89`, `DiscardCommand.java:96` |

Not yet processed: **R19-18** (Guest reuses the shop TO; `ShopInfo` access on the anonymous actor fails `transform` with `ObjectExpressionMatchesBinding`; generator rewrites a new actor's `application-customizer.tsx`; stale browser bundle).

## 2026-11-19: kb use in the webshop run (R18–R19)

Source: `webshop-run/2026-11-11T14-06-20-342Z_01a1caee-...jsonl.gz`, entries from 2026-11-19T07:30Z.

| Metric | Value |
|---|---|
| Tool calls | bash 557, browser 79, read 59, kb_search 25, kb_get 12 |
| Direct catalog reads/greps | 40 (most are whole-file reads of short entries, as the skill says) |
| kb calls after 13:11 | none until the end of the run (16:15): R19-15..18 were built without kb lookups |

### kb issues (for the kb developers)

1. **Wrong `parent` in `kb_search` results.** `Frontend Extension Points > Dashboard Page` (H2, line 41 of `agent-docs/frontend/extension-points.md`) is returned with `parent: "Frontend Extension Points > Extra Routes"`, a sibling H2 (line 13); the condensed `⤷` line shows the same. The agent built `... > Extra Routes > Dashboard Page` from it. Reproduced 11-19.
2. **`kb_get` with a wrong section reports the file as not found.** `kb_get("agent-docs/frontend/extension-points.md", "Frontend Extension Points > Extra Routes > Dashboard Page")` → `(not found: agent-docs/frontend/extension-points.md)`. Expected: "section not found" plus the file's section list. Reproduced 11-19.
3. **The frontmatter `meta` chunk wins and hides the body.** For `best-practices/backend/gdpr-placeholder-user-on-delete.md` the top hit is `chunkId …:meta` (headingPath = title, `suppressedSections: 4`); `kb_get` of that section returns the description plus the keyword list; a path-only `kb_get` returns the intro and "(+7 more sections)" without their names. Agents then read the file from disk (webshop R16-10, R16U-1, R17-1, R18-1). Reproduced 11-19.
4. **Weak ranking for some queries:** "database index on attribute unique identifier rdbms index" → `application-config.agent.md` and AGENTS indexes (the catalog fact was missing then: R18-2, since added); "root context redirect default application Karaf servlet / landing" → unrelated (catalog gap, filled by the `web-root` note in `frontend/README.md`).
5. **Usage, not a kb defect:** the build agent stopped using kb for the last three hours of the run; prompts must repeat "kb_search / kb_get first on any problem".

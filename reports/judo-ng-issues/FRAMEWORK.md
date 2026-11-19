# judo-ng framework: issues for the framework developers

Generators, templates, transformations, runtime and `judo.sh`. CLI issues are in [CLI.md](CLI.md).
judo-ng base: latest `develop` (worktrees in `target/judo-ng-read/wt/`); paths below are relative to it. The catalog documents the user-side workarounds.

| # | Issue | Repo | Source |
|---|---|---|---|
| 1 | Generated frontend imports a type twice; depends on actor order | runtime__judo-tatami-client (esm2ui Zeta), template__judo-ui-react-template | R16-1, R19-12, R19-17 |
| 2 | `XMI ID COLLISION DETECTED` for action ids in the ESM to UI transform | runtime__judo-tatami-client | R10-15, R19-17 |
| 3 | `anonymous` defaults to `true`: an actor created without the flag skips token checks | models__judo-meta-esm | R19-12 |
| 4 | `judo.sh build -M -B` stops and deletes Karaf, then builds only the frontend | template__judo-esm-fullstack-project-template | R19-12 (d) |

## 1. Duplicate type imports, depending on actor order

- **Behaviour:** the generated admin frontend contains `import type { CsvFile, CsvFile, CsvFileStored, CsvFileStored }`; `./judo.sh build` stops at `pnpm run format` (biome: `Declarations inside of a import declaration may not have duplicates`).
- **Reproduction (the app's own Maven pipeline, `mvn -o` on `frontend-react/model` then `<app>__admin generate-sources`):** the same commit with a third actor last in the model file: 48 admin files (12 pages) with duplicates; with that actor first: none.
- **Cause:** `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/zeta/Esm2UiZetaTransformation.java`
  - `:1720-1723` runs the transformation once per actor, in model file order, into one shared UI model.
  - `fixCallOperationActionDefinitions` (`:835-907`) collects the call-operation actions of **all** actors from the shared resource set (`:847-858`), looks up the `ClassType` by the name prefix before `::` in the **current** actor's application (`findContainerClassType`, `:1182-1197`) and calls `setOperation` with the current actor's copy (`:888`, `:907`).
  - So a later actor rebinds earlier actors' actions to its own operation copy: 126 cross-actor operation references in the failing model (36 from Admin), 54 with the actor first.
  - `template__judo-ui-react-template/judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/UiPageHelper.java:154` collects page imports in a `HashSet<ClassType>` (identity); `:181` adds the rebound output class next to the page's own copy, and the templates (`actor/src/dialogs/customization.ts.hbs:4`, `index.tsx.hbs:51`, `hooks.tsx.hbs:6`) emit one import per entry.
- **Expected:** an action keeps the operation of its owning actor (look up and rebind within the action's own application); the output does not depend on actor order. Defensive: deduplicate page imports by class name.
- **Workaround:** create the new actor at the first position; check the generated sources for duplicate imports after `generate`.

## 2. XMI ID collisions in the ESM to UI transform

- **Behaviour:** the frontend-react model step logs `[ERROR] XMI ID COLLISION DETECTED: ID 'Admin/(esm/<id>)/TabularReferenceFieldLinkCreateAction' is being reassigned from Action (obj@...) to Action (obj@...)` for five `TabularReferenceFieldLink*Action` ids of one tabular reference field, in every actor order; the build continues. A transform UI model also had 111 `xmi:id` values used twice, all on `icon` elements.
- **Expected:** unique ids, or no error-level log when the duplicate is harmless.

## 3. `anonymous` defaults to `true`

- **Behaviour:** `models__judo-meta-esm/model/model/esm.ecore:434-436` (`anonymous`, `defaultValueLiteral="true"`). An `ActorType` created without the flag and without a mapped principal is effectively anonymous (`esm.genmodel:506-507`): no realm, no Keycloak client, and `runtime__judo-runtime-core/judo-runtime-core-security-keycloak-cxf/.../KeycloakLoginInterceptor.java:138-139` verifies a bearer token only when the actor has a realm. Its accesses are public.
- **Expected:** a secure default (`false`), or a validation warning for an anonymous actor with accesses.
- **Related CLI symptom:** `managed` is then refused on that actor (`models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmFieldRules.java:425-428`) but stored as `true` (CLI.md #2).

## 4. `judo.sh build -M -B` leaves the application down

- **Behaviour:** `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:837-841` stops Karaf and runs `rm -rf $KARAF_DIR` whenever the Karaf package is built (default), before Maven; with `-M -B` the branch at `:850-851` then runs only `mvnd install -f frontend-react`. No model, backend or Karaf package is rebuilt, so the application stays down; a full build that fails in a later module leaves it down the same way.
- **Expected:** `-M -B` keeps Karaf (no package rebuild), or stops it only when a new package will be built.
- **Workaround:** `./judo.sh build -f` for a frontend-only build.

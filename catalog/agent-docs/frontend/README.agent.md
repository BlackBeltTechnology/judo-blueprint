# README.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/README.md.

## Overview
- React frontend generated from ESM + UI models; customize via hook system (Pandino), not by editing generated code.
- `<app>` = `app_name` in `judo.properties`. `[actor_fqn]`: model `<model>::service::Admin` → `service__admin` (lowercase, `::`→`_`).
- Module path: `application/frontend-react/<app>__[actor_fqn]/` (double `__` after app name).

## Key Concepts
- Model-driven generation; hook system on Pandino; register hooks instead of editing.
- Checksum protection: editing a generated file fails the build unless listed in `.generator-ignore`.
- `.default` scaffolds under `src/custom/hooks/...` (e.g. `src/custom/hooks/pages/register<Page>ActionsHook.ts.default`). Copy, drop `.default`. Hook scaffold only when matching model flag set (e.g. `generateActionsHook`).
- `src/custom/application-customizer.tsx` is a plain generated file (not `.default`).
- `src/custom/` written by actor module Maven build (`./judo.sh build`), NOT `./judo.sh generate`; fresh module has no `src/custom/` until first build.
- `*.ts.default` / `*.tsx.default` gitignored; `src/custom/` itself NOT gitignored: commit custom code.
- Generator writes four files without `.default`: `application-customizer.tsx`, `index.tsx`, `custom-element-types.ts`, `interfaces.ts`. Hand-edit → list in `.generator-ignore`.

## Architecture

### Routing
- Hash router (`createHashRouter`): pages at `/<app-path>/#/<route>`. Browser tests must use hash URL.

### Generated vs Custom Code
- Generated (do not edit): `src/containers/`, `src/pages/`, `src/dialogs/`, `src/components/`, `src/layout/`, `src/utilities/`, `src/auth/`, `src/App.tsx`, `src/routes.tsx`, API client services, model types. Custom routes go in `src/extra-routes.tsx`.
- Custom: `src/custom/` (hooks, customizations), `src/theme/`, `src/custom/application-customizer.tsx` (`customize(context)` registers Pandino services).

### Code Generation and Checksum Protection
- Tracked by checksum in `.generated-files-<actor>` (module root; one per actor).
- Files not in `.generator-ignore` regenerated on `./judo.sh build` / `mvn clean install`.
- Checksum mismatch (edited file) → build FAILS. Unchanged → regenerated.
- Last-resort edit of generated file: edit, then add path to `.generator-ignore`. Prefer hooks.
- Checksum errors from formatting/git checkout/Prettier/Biome: `mvn clean install -DvalidateChecksum=false` (module) or `./judo.sh build -i`.

## Project Structure
- Tree: `model/` (UI model pom, `target/generated-resources/model/<app>-ui.model`); `src/` (generated containers/pages/dialogs/components/layout/utilities/auth; `extra-routes.tsx`; `custom/` with `application-customizer.tsx`, `hooks/`, `components/`, `hooks/**/*.default`; `theme/palette.ts`; `App.tsx`); `public/i18n/` (`default`, `en-US`, `hu-HU`); `.generator-ignore`; `package.json`; `vite.config.ts`; `pom.xml`.

## Generation Process
- Flow: ESM model (edit only with Judo Designer) → UI model generation (`application/frontend-react/model/pom.xml`, plugin `judo-tatami-psm2ui-maven-plugin`) → React code generation (module pom, plugin `judo-ui-react-maven-plugin`) → pnpm/vite build (`frontend-maven-plugin`) → frontend JAR → auto-deploy to Karaf when server runs.
- See ../model/README.md for model details.

## Understanding .generator-ignore

### One Rule
- `.gitignore`-style, for generator output only. Purpose: stop re-emit of a path you hand-edited.
- Three cases:
  1. Generator emits X and you hand-edit X in place → add X. Only legit case (e.g. `src/pages/MyPage.tsx`, `src/theme/palette.ts`, stub `src/custom/application-customizer.tsx`).
  2. `.default` rename: generator emits `X.default`; rename to X once. X outside scope, no entry. Do NOT add `X.default`.
  3. Brand-new hand-written file the generator never emits at that path → no entry.
- Purely custom files in `.generator-ignore` = noise; remove.
- Location: `application/frontend-react/<app>__[actor_fqn]/.generator-ignore`. Syntax: `#` comments; exact path; globs `src/custom/**/*.tsx`; dirs `src/custom/`; patterns `*.custom.tsx`, `**/custom-*.tsx`.
- Verify: `grep <path> .generator-ignore`.

## Generated File Headers
- Header lines: `Factory expression`, `Path expression`, `Template name`, `Template file` (`.hbs` in `judo-ui-react-template` or `judo-ui-typescript-rest-template` artifacts).
- Template name = override key: override by same name in `generator-overrides/`. Factory = when regenerated. Path = output location.

## Code Generation Templates

### 1. judo-ui-typescript-rest-template
- TS REST client: `data-api/**/*.ts` (types, service interfaces), `data-service/*.ts` (implementations), axios clients (`data-axios` template, e.g. `accessServiceImpl`).

### 2. judo-ui-react-template
- Containers `src/containers/**/*.tsx` (path `src/containers/<containerPath>/<Component>.tsx`), `src/pages/*.tsx`, `src/components/**/*.tsx`, `src/dialogs/**/*.tsx`, `src/App.tsx`, `src/routes.tsx`, i18n, theme, hook placeholders.

### Template Override Process
- Use when hooks cannot achieve behavior. Steps: identify template name from header; `generator-overrides/<template name>.hbs` (e.g. `generator-overrides/actor/src/App.tsx.hbs`); `mvn clean install`.
- Overrides checked before defaults. Must be maintained on upgrade. Prefer hooks; document why.

### Template Variables
- `ui-react.yaml` per template: `name`, `templateName`, `pathExpression` (SpEL), `factoryExpression` (SpEL; one output per result), `applicationBased`, `conditionExpression` (skip when false), `copy`, `exclude`, `permission` (POSIX), `templateContext`.
- Context: `#self`, `#application`, `#applications`, `#model`, `#template`, `#addDebugToTemplate` (when `-DtemplateDebug`).
- Override layering: same name + new `templateName`/`pathExpression` replaces; `<name>.override.hbs` decorates (can include original as partial); `exclude: true` removes. Theme fragments: see theming.md.
- Helpers: `toSafeCamelCase`, `firstToUpperCase`, etc. `classDataName('MyPackage::MyClass', '')` → `MyPackageMyClass` (only first char uppercased per joined name).

## Related Documentation
- Authoring vs customizing: UI layout (Form/Table/View on TOs, menu on ActorType) is authored in ESM model → ../model/ui-authoring-guide.md.
- Core: development-workflow.md, theming.md, i18n.md, advanced-patterns.md.
- Hook system: hooks/README.md, hooks/data-hooks.md (usePrincipal, useViewData), hooks/ui-hooks.md (AppBar, Hero, Logo, Footer), hooks/table-hooks.md (row highlighting, custom columns, sidekicks), hooks/action-hooks.md (container/page actions, operation flows), hooks/navigation-and-access.md (redirects, access filtering, hotkeys), hooks/validation-hooks.md (date/datetime validation).
- Platform: error-handling.md (400/422/401/403/404/500, fault dialog, i18n keys), extension-points.md (extra routes, guest page, sub-themes, menu actions hook, app switcher, table state), build-and-deployment.md (Maven modes, MUI license, base href, checksums), ui-model-pitfalls.md (model values breaking generator, renames, E2E).

## External Documentation
- judo-ui-react-template docs (GitHub), judo-generator-commons README, MUI, Vite, React 19 docs.

## Best Practices
- Hooks over direct edits; `.generator-ignore` for protected edits; minimal customizations; test after regeneration; strict TypeScript; MUI patterns; use generated services (no reimplemented API calls); document custom hooks.

## Troubleshooting
- File overwritten after build → add to `.generator-ignore`.
- Checksum mismatch → (1) add to `.generator-ignore` and rebuild; (2) `git checkout <file>` and rebuild; (3) `mvn clean install -DvalidateChecksum=false` or `./judo.sh build -i` for formatting-only changes.
- Hook not called → check registration in `application-customizer.tsx`; export name matches interface.
- Type errors after regeneration → `pnpm install`; check breaking changes in generated types.

## File Locations Reference
- UI model: `application/frontend-react/model/target/generated-resources/model/<app>-ui.model`.
- Generated React: `application/frontend-react/<app>__[actor_fqn]/src/` (everything outside `src/custom/` and `.generator-ignore` entries).
- Custom hooks: `…/src/custom/`. Build output: `…/target/*.jar`. Vite config: `…/vite.config.ts`.

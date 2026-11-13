---
id: structure-frontend-unit-test-placement
title: Unit Test Placement in an Actor Frontend Module
description: Put unit tests for custom frontend code under src/custom next to the helper they test (or in one dedicated non-generated folder), keep the logic they test in pure helper files, and never add tests to generated folders or to .generator-ignore.
aliases: [frontend unit tests, custom code tests, test folder layout]
keywords: [unit test, vitest, __tests__, test.ts, colocated tests, src/custom, helper, generated utilities, pnpm test]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/__tests__", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/utils"]
alternatives: []
related: [shared-service-helper-module, custom-component-directory, structure-generator-ignore-scope]
fragment: "none: frontend-only"
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Custom frontend logic (masks, validation feedback, prefill rules) breaks silently when the model changes. Unit tests catch that, but only if they live where regeneration cannot touch them and where a reader finds them next to the code.

## Practice

### Platform base

- Files the generator never emits, including anything you add under `src/custom/`, are outside generator scope and need no `.generator-ignore` entry ([One Rule](../../agent-docs/frontend/README.md)).
- The agent-docs do not describe a frontend unit-test runner. In one example the generated module ships vitest, its own tests in `src/utilities/*.test.ts`, and a generated pom that runs `pnpm run --if-present test` in the Maven `test` phase: *verify* for your platform version.

### Practice notes: test pure helpers, next to the helper

```
src/custom/
  hooks/
    utils/
      formatAmount.ts
      formatAmount.test.ts        # unit test beside the helper
    dialogs/
      registerXActionsHook.ts     # thin wiring, rarely unit-tested
```

- Move the logic you want to test out of hook and component files into pure helper modules ([[shared-service-helper-module]]); test the helper, keep the hook a thin wiring layer.
- Put the test beside the helper as `<name>.test.ts`. If the team prefers one test folder, use a single non-generated folder such as `src/__tests__/` for everything, not both styles.
- Never place custom tests in generated folders (`src/utilities/`, `src/pages/` and so on): the generator owns those folders and already writes its own tests there.
- Do not list test files in `.generator-ignore`.
- Tests that pin generated output (for example, that a generated page still has a field your custom mask relies on) are useful upgrade guards; name them after the generated artifact they pin.

## Rationale

Helpers in `src/custom/` survive regeneration, and a test beside its helper moves and is deleted with it. One placement style means a reviewer knows where to look. Generated folders belong to the generator, so a hand-written test there is easy to mistake for generated code and can collide with a test the templates add later.

## Example

- One frontend has tests in `src/__tests__/` plus colocated `*.test.ts` files in `src/custom/hooks/utils/`, `hooks/pages/`, `hooks/dialogs/` and `hooks/`: two styles in one module, with some helpers tested in each place.
- One frontend's `viewGeneratedMasks.test.ts` reads generated pages as text and asserts that their masks still carry fields the custom code depends on, so a model change fails the test run instead of the running app.
- One frontend also lists test files in `.generator-ignore`, which the platform rule says is not needed ([[structure-generator-ignore-scope]]).

## When to avoid

- The actor frontend is fully generated or only re-registers generated behaviour: there is no custom logic worth a unit test; rely on E2E tests.

## Related

- [[shared-service-helper-module]] — extracting testable helpers from hooks
- [[custom-component-directory]] — the custom root the tests live in
- [[structure-generator-ignore-scope]] — tests need no `.generator-ignore` entry

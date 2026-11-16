---
title: UI Model Pitfalls
description: Model values and workflows that break the frontend generator, renames and retargeting fallout, and the model-driven, UI-first end-to-end test approach.
---

# UI Model Pitfalls and Model-Driven Frontend Work

Model values and workflows that break the frontend generator, and how to work model-first.

## Model Features Instead of Custom Components

Add a field, column or operation to the UI by modeling it: add the element to the View/Form/Table of the transfer object, then customize behaviour with hooks and overrides. Do not replace generated code with a whole custom component. New transfer object attributes and operations are not placed on forms and views automatically; each must be added explicitly as a data field or operation form.

## Values That Break the Generator

- `booleanWidget: "SWITCH"` does not exist; the generator fails with a missing `switch.hbs` partial. Use `CHECKBOX` or `COMBO`.
- Tabular reference field columns that reference attributes of an external transfer object or namespace on an unmapped input transfer object break the build.
- Wrapping operation forms in an action group on a view can fail UI validation; placing them directly on the view passes.

## Opaque UiValidationException

`UiValidationException: All constraints have been satisfied` is reported as an error but names no failing constraint. Bisect: remove all UI layout mutations to get a passing build, then re-add them one group at a time, rebuilding after each, until the culprit is isolated.

## Renames and Retargeting

Renaming an operation or retargeting a transfer object regenerates action and container files and hook scaffolds. Typical fallout: duplicate `updateAction` identifiers in a generated `types.ts` and `TS2307 Cannot find module '~/dialogs/...'` in custom hooks whose generated path disappeared. Old `.default` scaffolds remain until regenerated with `./judo.sh build -i`. After a rename regenerate, move customizations that live in a removed generated location, and update every reference to the old name. Retargeting a shared transfer object to a different projection changes its generated Stored type, which the frontend then rejects where properties are missing.

## End-to-End Testing Approach

Drive tests through the real UI (Playwright) and assert visible elements. Use REST-only checks just for authorization versus validation distinctions and hidden menu items. Create the database once from a base dump and derive test groups from it, keeping a run within about two minutes. Use the generated UI model to find what each view, table and form shows. See [E2E Testing](../e2e-testing/README.md).

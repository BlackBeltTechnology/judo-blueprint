---
id: table-row-action-icon-from-operation-form
title: Table Row and Bulk Action Icons Come From operationForm.iconName
description: "In the observed generator version the icon of a table row or bulk action is read from the child operation form's iconName, not from the table operation's own iconName; without it a chevron shows."
aliases: [row action icon, chevron_right icon, bulk action icon]
keywords: [iconName, operationForm, TableOperation, rowOperations, tableOperations, chevron_right, MdiIcon, row action]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: table
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model"]
alternatives: []
fragment: "none: frontend-only"
first_seen: 2026-07-09
last_updated: 2026-11-10
---
## Intent

Row actions and bulk toolbar actions of a table should show a meaningful icon. In the observed setup the icon comes from the child operation form of the table operation. Setting an icon on the table operation alone has no visible effect, and an operation form without icon renders `chevron_right`, a `>` glyph that looks like "no icon". The wrong state is hidden behind a plausible default, which makes the gotcha costly.

## Practice

### Platform base

- A `TableOperation` sits in `rowOperations` (one row) or `tableOperations` (toolbar, bulk with `isBulk`). It has its own `iconName` and contains an `operationForm` ([TableOperation reference](../../agent-docs/model/esm_metamodel/ui.md), [tables and navigation mapping](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)).
- `OperationForm` has an `iconName` too, documented as the button icon ([widget mapping](../../agent-docs/frontend/esm-to-ui-mappings/widgets.md)).
- The agent-docs list `TableOperation.iconName` as the action icon and say nothing about the operation form winning or about the `chevron_right` default. The rule below is an observation: *verify* it against your generator version.

### Practice notes: set the icon on the operation form

- Set the icon on the operation form inside every row and bulk table operation. Leave the table operation's own icon unset, so there is no dead configuration.
- Icon names are Material Design Icons slugs (hyphenated), for example `delete`, `pencil`, `repeat-variant`, `file-image-plus-outline`, `cash-plus`.
- The generated React shows the source. A row action renders an icon component with the operation form's name; a bulk action passes it as `startIcon`:

```tsx
// Example generated shape
<MdiIcon path="chevron_right" />            // operation form had no icon (default)
{ startIcon: 'close', isBulk: true }        // bulk action: icon from the operation form
```

- To diagnose, count the default glyph in a generated container: any `path="chevron_right"` on an action that should have an icon points at a missing operation-form icon.

## Rationale

- Knowing the real source avoids a class of "the icon will not show" debugging.
- The table operation is the obvious element to configure, and the default masks the miss.

## Example

In one project, icons first set on `rowOperations` and `tableOperations` kept showing `>` chevrons. Reading the icon component and a generated container (three `chevron_right` against one correct icon) showed that the operation form's icon is rendered. The fix set the operation form's icon per operation, following the app convention (`toggleActive` → `repeat-variant`, `edit` → `pencil`, `delete` → `delete`). The misplaced table-operation icons were then removed as dead configuration.

## When to avoid

- If your generator version renders `TableOperation.iconName` (as the agent-docs state), set that instead and skip the operation-form icon.

## Related

- [[custom-public-assets]] — brand, logo and image assets in the frontend

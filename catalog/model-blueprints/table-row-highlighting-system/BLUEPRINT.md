---
id: table-row-highlighting-system
title: Table Row Highlighting System
description: "Colors table rows by their data (an enumeration value or a flag) with a table row highlighting hook registered per generated table component; the model is not changed."
aliases: []
keywords: [table, row, highlighting, hook, pandino, color, legend, enum]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: "none: frontend-only"
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Make important rows stand out in a generated table without changing the model or the generated code. A hook returns named rules, each with a color and a condition on the row. The table paints matching rows and shows a legend entry per rule.

### Rules are data-driven

A rule has a `name`, a legend `label`, a `backgroundColor` and a `condition` that receives the row parameters. The condition reads the row's own attribute values, typically an enumeration value or a boolean flag ([table hooks](../../agent-docs/frontend/hooks/table-hooks.md#table-row-highlighting)).

### One hook per table

The hook is registered as a Pandino service under the table-row-highlighting key. The `component` service property names the generated table component it applies to. A hook without the right component name does nothing.

## Structure

Frontend only. No entity, transfer object or enumeration is added. The pattern needs a table whose rows carry the attribute the rules test. For each table that should be colored:

- A hook function that returns the array of rules.
- A registration in the application customizer with the generated table component name as the `component` property.

The hook type, its key and the stored-row type come from the generated theme and data-API model, not from project code. The folder for hook files and the file names are project convention.

## Constraints

- One registration per table component. Different tables get different hooks.
- The condition only sees the row data the table already loaded. Attributes not shown by the table's transfer object are not available.
- Enumeration values arrive as the generated values, so compare against the enumeration member and not against the label.
- Only the background color can be set. Icons or badges need a custom column or a visual element override.
- Colors are hard-coded in the hook. Keep them in one shared constant when several tables use the same scheme.
- The condition must be cheap and null-safe. It runs for every visible row.

## Variations

- **Several rules per table.** One hook returns several rules, such as one color per enumeration value.
- **Threshold rules.** The condition compares a number or date, for example overdue rows.
- **Shared palette.** Hooks for many tables take their colors from one module.
- **Add a column.** To show a badge or icon beside the color, add a custom column. See [[table-row-highlighting-hook]].

## When to use

- Rows must be told apart by an enumeration, status or threshold.
- The generated table is kept and only its look changes.
- The same attribute drives a legend the users should see.

## When to avoid

- The color must carry information that cannot be read by a color-blind user. Add a text or icon column.
- The table should hide or filter rows by the condition. Use a query or filter instead.
- The decision needs data outside the row, such as another entity. Compute it in a derived attribute of the row first.

## Related

- [[table-row-highlighting-hook]] — the best-practice version with the hook shape
- [[pandino-action-hook-override]] — the same registration mechanism for action hooks
- [[application-customizer-hub]] — where all hooks are registered
- [[custom-visual-element-override]] — when more than a background color is needed

---
id: "table-row-action-icon-from-operation-form"
title: "Table Row/Bulk Action Icons Come From operationForm.iconName"
domain: "frontend"
category: "table"
score: 31.0
usage_count: 1
alternative_count: 0
first_seen: "2026-07-09"
last_updated: "2026-07-09"
projects:
  - rackinspect
---
## Description

The icon rendered for a table **row action** (and **bulk toolbar action**) is driven by the child `operationForm.iconName`, **not** by the `TableOperation` / `<rowOperations>` `iconName`. Setting the icon on the TableOperation alone has **no visible effect** — the generator reads the operationForm's icon. An operationForm with no icon defaults to `chevron_right`, which renders as a `>` glyph and looks like "no icon".

This is a common and costly gotcha because the "obvious" element to configure (the TableOperation) is the wrong one, and the wrong state is masked by a *plausible-looking default* (`chevron_right`) rather than a blank.

## Structure

```
# WRONG — sets icon on the TableOperation; row action still shows a chevron
update(fqn: "…::Rack_Table::deleteRackTableOperation",
       input: { tableOperation: { iconName: "delete" } })

# RIGHT — set the child operationForm's icon (what the generator renders)
update(fqn: "…::Rack_Table::deleteRackTableOperation::deleteRack",
       input: { operationForm: { iconName: "delete" } })
```

Generated React confirms the source:
```tsx
// row action -> MdiIcon path="<operationForm.iconName>"
<MdiIcon path="chevron_right" />           // operationForm had no icon (default)
// bulk action -> startIcon: '<operationForm.iconName>'
{ startIcon: 'close', isBulk: true, ... }  // from operationForm, not TableOperation
```

Icon names are Material Design Icons slugs (hyphenated, `@mdi/font`), e.g. `delete`, `repeat-variant`, `file-image-plus-outline`, `cash-plus`, `pencil`.

## Examples

### RackInspect
Row/bulk action icons initially set on `<rowOperations>`/`<tableOperations>` iconName had no effect — the UI kept showing `>` chevrons. Inspecting `src/components/MdiIcon.tsx` and a generated container (`MdiIcon path="chevron_right"` ×3 vs a correct icon ×1) proved the render source is `operationForm.iconName`. Fix: set `operationForm.iconName` per operation, matching app conventions (`toggleActive` → `repeat-variant` in 17 places, `edit` → `pencil`, delete → `delete`, `addPicture` → `file-image-plus-outline`). The wrongly-placed TableOperation icons were then removed as dead config.

## Trade-offs

- Pros: knowing the real source avoids a whole class of "icon won't show" debugging.
- Cons: the icon lives one level deeper than intuition suggests; the `chevron_right` default hides the gap.
- Prefer when: modeling any row/bulk `TableOperation` that should show a meaningful icon.

## Related Patterns

- [custom-public-assets](custom-public-assets.md) — brand/logo/image assets in the frontend

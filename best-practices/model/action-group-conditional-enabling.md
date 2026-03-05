---
id: "action-group-conditional-enabling"
title: "ActionGroup with Conditional Enabling and Featured Actions"
domain: "model"
category: "ui"
score: 11.9
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
---
## Description

ActionGroups in the JUDO UI model group related operation buttons together with support for conditional enabling based on derived boolean attributes, featured action highlighting, and page-state-aware disabling. An ActionGroup can be dynamically enabled/disabled using an `enabledBy` reference to a derived boolean attribute, promoting a subset of its actions as "featured" (shown prominently), and adapting its behavior based on the current page state (view vs edit).

## Structure

- **ActionGroup element** groups related `Button` actions within a Flex container
- Key properties:
  - `enabledBy`: References a boolean attribute (often DERIVED) that controls whether the group is enabled
  - `featuredActions`: Integer specifying how many of the first N actions are displayed prominently
  - `disabled`: Force-disables the group (used in Edit pages to prevent operation invocation during edits)
  - `isReadOnly`: Sets the group to read-only mode (used in View pages)
  - `icon`: Visual icon representing the group's purpose
  - `label`: Display name for the group
  - `fit`: Layout fitting mode (e.g., LOOSE)
- Actions within the group are `Button` elements bound to `CallOperationAction` via `dataElement` references
- ActionGroups are replicated across device layouts (mobile, tablet, desktop, default) with responsive column adjustments

```xml
<ActionGroup name="actionGroup" label="Play God"
  enabledBy="AttributeType@.../Planet/habitable"
  featuredActions="2" icon="weather-sunset">
  <actions xsi:type="ui:Button" name="createCreature" .../>
  <actions xsi:type="ui:Button" name="destroyLife" .../>
  <actions xsi:type="ui:Button" name="startWar" .../>
  <actions xsi:type="ui:Button" name="endWar" .../>
</ActionGroup>
```

## Examples

### ActionGroupTest
"Play God" ActionGroup on Planet views with `enabledBy="Planet.habitable"` (derived boolean) and `featuredActions="2"`. Groups 4 actions: createCreature, destroyLife, startWar, endWar. First 2 are featured (prominent buttons), last 2 are secondary. Enabled only on habitable planets. Disabled in Edit pages, read-only in View pages. Appears in 8 page variants across 4 device layouts.

## Trade-offs

- Pros: Logical grouping of related actions, conditional enabling driven by model state, featured actions provide visual hierarchy, responsive across devices
- Cons: Same ActionGroup must be replicated across device layouts, limited to single-attribute enabling condition (no compound expressions)
- Prefer when: Multiple related operations share an enablement condition and benefit from visual grouping with a primary/secondary action hierarchy

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md) (provides the derived boolean attributes used by enabledBy)
- [ui-control-transfer-fields](ui-control-transfer-fields.md) (similar UI-state-from-model approach)

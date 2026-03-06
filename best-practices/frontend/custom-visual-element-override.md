---
id: "custom-visual-element-override"
title: "Custom Visual Element Override via Pandino"
domain: "frontend"
category: "component"
score: 59.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - workflow-poc
---
## Description

Replace a generated UI group or table component within a page with an entirely custom React component using the `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` Pandino service registration. This is the most powerful customization mechanism in JUDO -- it allows swapping out a specific section of a generated page (identified by a component key) with a hand-built React component while keeping the rest of the page generated.

## Structure

```typescript
// In application-customizer.tsx
import { CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY } from '~/theme';
import { MyCustomComponent } from './hooks/custom-implementations/MyCustomComponent';

context.registerService(
  CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY,
  MyCustomComponent,
  { component: 'ServicesEntityEntity_View_EditGroupName' }
);
```

The custom component receives the same props as the generated component (data, editMode, storeDiff, etc.) and can render any React UI.

```typescript
// Custom component implementation
export const MyCustomComponent: FC<CustomProps> = ({ data, editMode, storeDiff, isLoading }) => {
  return (
    <Box>
      {/* Custom rendering of the group/table */}
    </Box>
  );
};
```

## Examples

### RackInspect
13 custom visual element registrations replace generated groups: DimensionParametersViewComponent (1,756 lines, renders configurable parameter forms with 4 value types), VAT ID input masking with `react-imask` (mask `00000000-0-00`), exchange rate password input, cost price data forms, and picture upload buttons. The dimension parameters component supports both "lazy" (immediate persistence) and "greedy" (batch on submit) modes.

### workflow-poc
2 custom visual elements registered via `componentImplementation` property: `'Mermaid'` renders workflow state diagrams as interactive SVG with `mermaid` + `svg-pan-zoom`, and `'Code'` renders YAML workflow models with `react-syntax-highlighter` (Prism `oneLight` theme). Both use `boundAttributeName` to read data from the transfer object dynamically.

## Trade-offs

- **Pros**: Maximum customization of specific page sections; rest of page remains generated; clean separation via Pandino component key
- **Cons**: Custom component must handle all edge cases the generated one did; no automatic updates from generator; tight coupling to page structure
- **When to use**: When a specific form group, table, or section needs UI that cannot be achieved through hook overrides alone

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [application-customizer-hub](application-customizer-hub.md)

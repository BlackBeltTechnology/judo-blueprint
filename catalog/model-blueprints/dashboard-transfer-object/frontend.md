## Overview

A dashboard transfer object can carry heavy frontend customization: a custom statistics view with KPI cards and a sortable table, and extra toolbar buttons such as a CSV export. The generated page is replaced in code, so this is application code.

## Implementation Pattern

- **Custom visual element.** A custom component can replace the generated statistics view, but only when the UI model declares that view as a custom implementation element. The component is then registered under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with the element's generated `component` key ([advanced patterns](../../agent-docs/frontend/advanced-patterns.md), Component Replacement Hook). In the reference implementation the component fetches its own data through the generated query and renders cards and tables.
- **Page mask** (common practice). A relation that the generated view does not fetch needs a mask override in the page actions hook. Without it, the nested relation is missing from the data.
- **Container actions.** Extra toolbar buttons on the dashboard are added through the container's generated actions hook (`<Container>ContainerHook`, see [action hooks](../../agent-docs/frontend/hooks/action-hooks.md)). Keep the button action to one operation call.
- **Hook keys.** Hook and override keys are generated per page or container, not per model element. Check the generated file for the exact key before writing an override, because the same element name can appear on more than one page.
- **Generator protection.** A file the application overrides must be listed in `.generator-ignore`, or the generator overwrites it.

```tsx
export const StatisticsView = ({ data }: { data: Statistics }) => (
  <Grid container spacing={2}>
    <Card title="Users" value={data.totalUsers} />
    <Card title="Active" value={data.activeUsers} />
  </Grid>
);
```

`Card` and `StatisticsView` are application components. The `data` shape comes from the generated query.

## Examples

### Variant seen in practice
- Framework: React
- Pattern: the statistics component is registered as a custom visual element on the dashboard. It fetches data on its own and renders KPI cards and a sortable table for per-organization statistics. The generated statistics form is replaced at the container level.
- Notable: the statistics mask includes 16 count attributes and a nested per-organization relation, so both the inline view and the page-level mask need an override.

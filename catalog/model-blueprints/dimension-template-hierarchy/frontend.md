## Overview

A template-driven form is a common frontend case: the generated table for a group is replaced by a custom component that builds its fields from the template's value types. The generator-protected files are project code.

## Implementation Pattern

- **Custom visual element.** A dynamic form component replaces the generated table for a group, in both edit and view mode. This works only where the UI model declares the element as a custom implementation; the component is registered under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with the element's generated `component` key ([advanced patterns](../../agent-docs/frontend/advanced-patterns.md), Component Replacement Hook), once for each page where the group appears. It renders one accordion per group, and one input per parameter chosen by the parameter's value type: numeric, text, boolean or a selection.
- **Selection inputs.** An ENUM parameter uses a relation input that lists the selectable values from the template.
- **Multi-row groups.** A group flagged as multi-line gets add and delete row actions. Each row copies the template parameters.
- **Helper module (project code).** A helper module holds the template-to-instance mapping: fetch the template parameters, copy them into the instance, and handle value changes.
- **Hook keys.** Hook and override keys are generated per page or container. Check the generated file for the exact key before writing an override.
- **Generator protection.** Each file the project overrides must be listed in `.generator-ignore`, or the generator overwrites it.

```tsx
const ParameterInput = ({ parameter, value, onChange }: Props) => {
  switch (parameter.valueType) {
    case 'NUMERIC': return <NumericInput value={value} onChange={onChange} />;
    case 'BOOLEAN': return <Checkbox checked={!!value} onChange={onChange} />;
    default: return <TextField value={value ?? ''} onChange={onChange} />;
  }
};
```

`ParameterInput` is project code. The `valueType` values come from the generated enumeration.

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/custom-implementations/DimensionParametersFormComponent.tsx`, `custom/hooks/custom-implementations/DimensionParametersViewComponent.tsx`, `custom/hooks/utils/dimensionTemplateHelper.ts`, `custom/hooks/dialogs/registerServicesDimension_serviceDimensionTemplateGroupsRelationFormPageActionsHook.ts`, `generator-overrides/ui-react/actor/public/i18n/application_default_extra.fragment.hbs`
- Pattern: the view component renders an accordion per dimension group with one input per parameter. The same components are registered on several pages, each with its own data source.
- Notable: the view component is the largest custom component in the project, and the helper module handles the full template-to-instance lifecycle, including row identity and lazy saving of persisted rows.

## Frontend guidance

### Show content and diagram with custom widgets

The version's content (definition text) and diagram (diagram source) are long text. The source project replaces their default widgets with a syntax-highlighted code viewer and an interactive diagram viewer, both registered under the custom visual element key in the application customizer (see [[custom-visual-element-override]], [[application-customizer-hub]] and the [UI hooks guide](../../agent-docs/frontend/hooks/ui-hooks.md)). This is optional polish.

### Lifecycle through generated actions

Upload, commit and publish appear as generated operation buttons on the admin pages. No custom hook is needed. The upload button opens the generated input form with the file field.

### Hiding is not protection

Hide the create and edit forms of versions, but rely on the operations, not hidden buttons, for state rules.

## Examples

### Example

- React frontend, two custom components for the content and diagram attributes.

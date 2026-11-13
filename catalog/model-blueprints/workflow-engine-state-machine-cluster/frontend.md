## Frontend guidance

### Replace two attribute widgets

The WorkflowVersion `diagram` and `model` attributes are long text. The source project replaces their default widgets with two custom components registered as Pandino services under the custom visual element key (see [[custom-visual-element-override]] and the [UI hooks guide](../../agent-docs/frontend/hooks/ui-hooks.md)), all registered in the application customizer (see [[application-customizer-hub]]):

- a diagram viewer that renders the diagram attribute as an interactive, pannable and zoomable state graph;
- a code viewer that shows the model attribute as syntax-highlighted text with line numbers.

Both receive the bound attribute name through their props and show a spinner while data loads. The registration pattern is documented for the platform; binding it to a data attribute, as here, is project practice.

### Navigate after an operation

Task operations (navigate, startWorkflow) return a redirect result carrying the target actor, access and id, or an operation to reload. The source project adds a small flow manager that consumes these results, and overrides a generator fragment so operations whose output transfer object carries a redirect annotation call it automatically. Treat the generator override as project-specific work; check the generator documentation before copying.

### Generated pages

Keep the task list and task views; hide generated forms for the engine entities, since they are not createable or updateable.

## Examples

### Example

- React frontend with two custom components (diagram viewer, code viewer), a redirect flow manager and one generator override.

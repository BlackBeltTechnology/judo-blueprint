## Overview

The task list and the task pages are generated. The example project adds one navigation handler, so that the result of a navigate operation opens the related domain entity. It also adds a template change, so that operations with a redirect output move the user after the action completes.

## Implementation pattern

- **Generated pages.** The list page shows the user's own tasks and the full pool. Count badges come from the TaskList counts. Action buttons for checkout, release, assign, execute and navigate are generated. Their visibility comes from the guard attributes, so no hook is needed for that.
- **Operation flow handler.** The example registers a flow handler that reads the result of an operation. When a result carries an identifier pair, the handler builds a filter for the target entity and opens its page. When a result refers to another operation, the handler reloads or redirects after the transition.
- **Redirect after an action.** The example overrides one generator fragment, so that operations whose output carries a redirect annotation call a redirect handler after the action completes.
- **Hook keys are generated per page or container.** Any custom hook that targets these pages must use the key that the generator produces for that page. Do not copy a key between pages.

## Examples

### Example

- Framework: React (example project code).
- Key files: `custom/application-customizer.tsx` (registers the flow handler) and `generator-overrides/ui-react/actor/src/fragments/operations/operation-primary-output-handler.fragment.hbs` (adds the redirect call).
- Navigate: the response carries the identifier name and value, and the handler turns them into a filter on the target page.
- Execute and start: the response refers to an operation, and the handler reloads the list or opens the next page.

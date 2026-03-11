## Overview

The Task List with Checkout/Release pattern manifests in the React frontend through an OperationFlowManager that handles redirect results from task operations (especially `navigate`), and a generator override that processes redirect-annotated operation outputs to route the user to the associated domain entity page.

## Implementation Pattern

- **OperationFlowManager**: Registered in `application-customizer.tsx` via `OPERATION_FLOW_MANAGER_INTERFACE_KEY`. The `handleResult` callback inspects operation results for `idName`/`idValue` pairs (used by `navigate` to redirect to domain entities) and `operation` references (used by `execute`/`startWorkflow` to reload or redirect after state transitions). It constructs `filterRecords` for entity lookup or passes through `access`/`actor` for page resolution.
- **Generator override for operation output handling**: A Handlebars template override (`operation-primary-output-handler.fragment.hbs`) injects a `processRedirect(result)` call when the operation output TO has a `redirect` annotation. This enables the generated action button handlers to automatically navigate after checkout, release, assign, execute, or navigate operations.
- **Generated task UI pages**: The generated frontend renders TaskList and Task pages with tables for myTasks/allTasks, count badges, and action buttons for checkout/release/assign/execute/navigate. Boolean guard attributes (isCheckoutEnabled, isReleaseEnabled, isNavigable, etc.) control button visibility without custom hooks.

## Examples

### workflow-poc
- Framework: React
- Key files: `custom/application-customizer.tsx`, `generator-overrides/ui-react/actor/src/fragments/operations/operation-primary-output-handler.fragment.hbs`
- Pattern: The OperationFlowManager handles `navigate` results by extracting `idName`/`idValue` from the response (CreateRedirect/UpdateRedirect TOs) and building a filter query to open the target domain entity page. The generator override adds `processRedirect` calls for redirect-annotated outputs.
- Notable: The task lifecycle operations (checkout, release, assign, execute, navigate) are fully generated -- only the redirect/navigation flow after operations requires custom code via the OperationFlowManager and generator override.

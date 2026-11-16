## Overview

The task has a close form in the author and approver views. The example project changes the result choices in that form so the initial state cannot be chosen when closing a task. The example also adds localized labels for the task forms, enumerations and menu items.

## Implementation pattern

- **Hook keys are generated per page or container.** The hook that customizes the close form is registered under an interface key that the generator creates for that page. The key is not a fixed platform constant, so look it up in the generated code of the page you customize.
- **Filtering enumeration options.** The hook returns a `filterResultOptions` function that removes the initial state from the result list. Without it the form shows every state, including the initial one, which makes no sense when closing a task.
- **Per-view coverage.** The filter is registered only for the author view in the example. The approver view uses the generated defaults unless a second hook is registered for its own page.
- **Localization.** The translation file gives labels for the close form, the approval form, the enumeration values and the menu items.

## Examples

- Framework: React with a plugin-based hook registry (example project code).
- Pattern: a close-form hook for the author task view.
- The hook receives the owner data, the form data, the edit mode, the store diff, the submit function and the submit callback. It returns `filterResultOptions`, which filters out the initial value of the TaskState enumeration.
- A locale file translates the close form title and result field, the approval form title, the TaskState and TaskType values, and the menu entries.

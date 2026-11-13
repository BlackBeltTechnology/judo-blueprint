## Overview

The user entity appears in the React frontend in two places. The profile panel shows the user's own data and lets the user change notification settings. The rest of the application checks the user's role to decide what to show.

## Implementation pattern

- **Profile panel.** A custom view replaces the generated profile form. It shows the name, the email and a link to the organization as read-only fields. Notification settings are switches that save on change, without an edit mode.
- **Role-aware display.** The current principal's role decides which actions are shown. A role check hides an action; it does not replace the server-side check.
- **Organization link.** The profile panel links to the organization's detail page.
- **Passwordless setup.** The profile panel has a button that starts passkey setup.
- **Hook keys are generated per page or container.** A custom hook must use the key that the generator produces for its page or container ([Advanced frontend patterns](../../agent-docs/frontend/advanced-patterns.md#page-and-container-action-hooks)).

## Examples

- Framework: React (example project code).
- The profile view uses switches for the notification flags, and it saves each change after a short debounce.
- The view reads the principal's role to decide which actions to show.

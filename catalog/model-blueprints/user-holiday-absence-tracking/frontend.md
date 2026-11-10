## Overview

The holiday list and the holiday form are part of the user's own panel. A date-range form creates a holiday, and the panel shows the existing ranges. Before a holiday is saved, the form shows any reservation that the range would cancel.

## Implementation pattern

- **Date range form.** The form takes a start date and an end date. It rejects an end before the start on the client, and the server rejects it again.
- **Conflict preview.** When the range changes, the form asks for the reservations inside it. If there are any, the form shows them and asks the user to confirm before creating the holiday.
- **Holiday list.** The panel shows the user's holidays, and a delete action is visible only for holidays the user may remove. The visibility comes from a guard attribute on the holiday.
- **Hook keys are generated per page or container.** A custom hook must use the key that the generator produces for its page or container. Do not copy keys between pages ([Advanced frontend patterns](../../agent-docs/frontend/advanced-patterns.md#page-and-container-action-hooks)).

## Examples

### park-here

- Framework: React (example project code).
- The panel uses the generated list and form for holidays. The conflict preview is a custom step before the create action.
- The panel shows the reservations that will be cancelled, so the user can see the effect before confirming.

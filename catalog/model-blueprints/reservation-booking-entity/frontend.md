## Frontend guidance

The source project replaces the default list tables and customizes the create form. All hooks below are project code, registered under the keys the framework generates for each page and container. Do not copy keys from another page.

### Cards instead of tables

Register a cards configuration hook for each reservation list (active, previous). The card element renders one reservation. See [[cards-container-configuration-hook]].

- The active card shows start, live current time and end on a timeline, the resource, the guest name or the vehicle id, and the delete, cancel and modify buttons.
- Show a button only when the row's guard attributes allow it. A card with both guards true is shown dimmed and inert.
- The previous card is a compact row: date and time range, resource, reserver and the translated status.

### Create form behavior

A dialog form action hook on the input form sets the defaults and the field behavior:

- on user change, pick the booking type and the preferred resource, and set the default times;
- filter the type options to the types the user may book;
- show or hide the guest and long-booking fields by type;
- recompute start and end when the date changes, and warn on odd start times;
- fill the form from the template data after it loads;
- return min and max constraints for the date and time pickers.

See [action hooks](../../agent-docs/frontend/hooks/action-hooks.md) and [validation hooks](../../agent-docs/frontend/hooks/validation-hooks.md). These checks are a convenience. The service enforces the same rules on the server.

### Modify form

A simpler hook pre-fills start and end from the owner data (the current reservation).

### Shared helpers

Keep the date and type logic in one helper module (for example `ReservationInputServices.ts`, an example name): default times, type choice from permissions, type-option filtering, favorite-resource check through the range API, and the noon minimum for quick bookings. The hooks stay thin and call the helpers.

Framework in the source project: React.

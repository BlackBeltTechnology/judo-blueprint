## Frontend guidance

### Generated pages

- Keep the generated Venue table and view pages for administrators; the slot collection appears as an inline table on the venue, where slots are added through the generated creation action.
- Keep the Slot form for physical descriptors (floor, wall, plan image, flags).
- Hide the generated Reservation create pages from members; members book through a dedicated booking form whose slot field uses the reference range.
- The preferred-slot field on the member profile is a relation with a range selection dialog; the dialog lists whatever the range interceptor returns, so no frontend filtering is needed.

### Hiding is not security

Hiding the exclusive-slot toggle or the venue access table from non-administrators is a convenience only. The backend range interceptor and the access definition of the actor decide what is reachable (see [backend.md](backend.md)).

## Examples

### park-here

- React frontend with generated pages; the booking form and the profile page use the slot range selection.

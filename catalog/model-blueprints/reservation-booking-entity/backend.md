## Backend guidance

Reservations are written only by custom operations on transfer objects: create, cancel, delete and modify. Operation bodies, the shared service and the e-mail service are project code, not platform API.

### One service behind thin operations

The operation classes are small components. Each delegates to one shared reservation service (example name `ReservationService`) and to an e-mail service. The service holds validation, permission checks, conflict detection, quotas and the DAO calls. Custom operations are never intercepted, so every rule must be in the service. See [interceptors](../../agent-docs/backend/interceptors.md).

### Validation the model cannot express

The service checks required fields, the user's permission for the chosen type, guest data completeness, time validity (not past, end after start, minimum length), quick-booking time limits, slot availability and the per-user quota per type. Availability is a DAO query on the resource and time range. See [data access guide](../../agent-docs/backend/data-access-guide.md).

### Lifecycle writes

- Cancel sets status EXPIRED and the end time to now.
- Delete sets status DELETED.
- Modify marks the old row DELETED and creates a new one (copy-on-write).
- A LONG booking creates one row per working day. The working-day helper is project code.
- Every write sets `modified` and `modifiedBy`. Enumeration values travel as ordinals on the wire; see [platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md).

### Range interceptors for choices

On the create input, range interceptors filter the resource and vehicle choices to what the user may use and what is free. A range interceptor fires only for reference range calls, so it is a filter for choices and the security boundary for those relations. It does not guard the custom operations. See [[interceptor-range-override]].

### Notifications

E-mails for create, delete, modify and reminder are rendered from stored templates. See [[platform-email-template-service]]. A scheduled job reads the reminder flags.

### Logistics variant

The freight variant has no custom create operation. An interceptor on the built-in create wires the acting partner into the new reservation. This works because create is a built-in operation; interceptors do not run for custom ones.

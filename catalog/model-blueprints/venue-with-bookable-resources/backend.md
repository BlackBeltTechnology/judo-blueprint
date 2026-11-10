## Backend guidance

### Narrow the slot range in a range interceptor

Choosing a slot on a booking form or on the preferred-slot field is a reference range operation. A range interceptor, an operation-call interceptor that fires on the `_getRangeReference*` operations, is where the access rules live. It fires only on these built-in range calls, not on plain list or query calls, and it never runs for custom operations (see [interceptors](../../agent-docs/backend/interceptors.md)). The interceptor keeps the incoming filter and ordering of the query customizer and adds constraints on top:

- only slots of venues the member may use (accessedVenues);
- only active slots;
- only free slots for the requested day or date range (project practice: two free-slot queries, one for a single day and one for several days, chosen by the booking type);
- exclusive slots only for administrators.

### Strip sensitive fields from the member template

The member-facing settings template contains venues. A post-call interceptor on the template call removes venue fields members must not see (notification template, access list, active flag). This is project practice on top of the platform interceptor mechanism; see [[interceptor-template-postcall]].

### Seeding and first-login provisioning

Venues and slots are seeded by an initializer in project code. An authentication interceptor creates the Member on first login from identity claims and marks configured administrator emails as administrators (project practice, configured through component properties). The class names in the source project (`InitCustomImplementation`, `LogAuthenticationInterceptor` and the range interceptors) are example project code.

## Examples

### park-here

- Three range interceptors narrow the slot choice on the reservation input and on the preferred-slot field; one template interceptor strips venue fields; one authentication interceptor provisions users.
- The interceptors preserve the original filter and ordering and add access constraints.

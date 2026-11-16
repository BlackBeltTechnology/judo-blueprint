## Backend guidance

### One service owns the feed rows

A single application service (not platform API) creates and removes the rows through the generated data-access objects (DAOs). Publishing a source item creates its rows. Deleting or expiring the item removes them. Operations do not write feed rows directly.

- Provide one create method per content kind, and one delete method per content kind.
- Each create method copies the display fields from the source and sets the type discriminator.
- Targeting is a strategy chosen by the content kind: one strategy for items shown to all active organizations, another for items shown only to organizations with matching capabilities.

### Write the rows in the publishing transaction

Interceptors run only for the platform's built-in operations (create, update, delete, list and so on), so the publish and unpublish custom operations call the feed service themselves. Call it after the source item is saved, inside the same transaction, so the feed and the source commit or roll back together.

### Keep targets in step with new organizations

When a new organization is created, add it as a target to the existing rows that it may see. Do this for that one organization only; a full pass is for repair.

### Bulk re-sync is a repair tool

Provide one custom operation (a static operation with a custom implementation) that re-syncs every row against the current targeting rules, for example after a rule change. Run it on demand. It is not the normal write path.

### Errors

A failed feed write is a platform failure. Fail the publishing operation so the source and the feed stay consistent. Do not throw a business fault for it, and never a bare `RuntimeException` for a user-facing problem.

## Examples

### Variant seen in practice

- A feed service has create and delete methods for each content kind (announcement, news, offer, request) and a targeting strategy per kind.
- Requests reach only organizations with matching capabilities. The other kinds reach all active organizations.
- The admin dashboard triggers the bulk re-sync operation.
- The application's own service and strategy classes are application code. Copy the pattern, not the names.

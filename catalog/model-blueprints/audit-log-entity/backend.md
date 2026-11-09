## Backend guidance

### Write audit rows from custom operations

Interceptors run only for built-in operations (create, update, delete, list and similar). Custom operations and script operations get no interceptor around them. So an audit row for a custom operation has to be written by that operation. Put the call last, after the business action, inside the operation's transaction.

- Keep one shared audit service with two methods: one that resolves the current user and organization from the security context, and one for automated actions that have no user.
- Each custom operation calls the service once with the action type, entity type, entity id and a details map.
- Serialize the details map to JSON in the service, not in each operation.
- The service looks up the organization name and writes it with the user name.

### Keep audit failures from breaking the business action

Wrap the audit write in a try/catch that logs the error and returns. A failure to write the audit row must not roll back a business change. See [[safe-failure-pattern]].

### Built-in operations: audit with an interceptor

If every built-in create, update and delete must be audited, a post-call interceptor can write the row. It runs inside the operation's transaction, so it must not throw a checked fault. Interceptor faults use `InterceptorCallBusinessException` (the business wrapper used by interceptors), not a generated fault class. An interceptor cannot cover custom operations, so keep the explicit calls too.

### Export as a file

A custom operation can export the log as CSV for the admin dashboard. It queries the entries with an optional date filter, writes the CSV with a UTF-8 byte-order mark, and stores the file with the platform file store service. The file store service is a platform service, so inject it with a reference.

### Project code, not platform API

The example project uses its own service classes around the audit log (an audit service, a DAO, a user lookup). These are project code. Copy the pattern, not the names.

## Examples

### mlszksz-platform

- Shared audit service in `common/services`, used by every custom operation of the project (59 at the time of writing).
- The enumeration covers 32 domain events, for example user login, post published and organization created.
- The export operation stores its CSV through the file store service.

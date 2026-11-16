## Backend guidance

### Write audit rows from custom operations

Interceptors run only for built-in operations (create, update, delete, list and similar). Custom operations and script operations get no interceptor around them. So an audit row for a custom operation has to be written by that operation. Put the call last, after the business action, in the same operation call.

- Keep one shared audit service (application code) with two methods: one that resolves the current user and organization from the actor context, and one for automated actions that have no user. The platform offers a variable resolver for the actor context; the service itself is yours.
- Each custom operation calls the service once with the action type, entity type, entity id and a details map.
- Serialize the details map to JSON in the service, not in each operation.
- The service looks up the organization name and writes it with the user name.

### Keep audit failures from breaking the business action

Wrap the audit write in a try/catch that logs the error and returns. A failure to write the audit row must not roll back a business change. See [[safe-failure-pattern]].

### Built-in operations: audit with an interceptor

If every built-in create, update and delete must be audited, a post-call interceptor can write the row. This is a variation for built-in operations only: the interceptor never runs for custom operations, so keep the explicit calls too. Synchronous interceptors run inside the operation's transaction, so an exception from the interceptor rolls the operation back; to refuse something it must throw `InterceptorCallBusinessException` (HTTP 422), because the generated checked fault exception cannot be thrown from an interceptor. Wrap the audit write so that a logging failure is not raised, if the business action must survive it.

### Export as a file

A custom operation can export the log as CSV for the admin dashboard. It queries the entries with an optional date filter, writes the CSV with a UTF-8 byte-order mark, and stores the file through the file store. Binary content travels to and from the client through file store tokens; see the platform behavior reference in the agent-docs.

### Application code, not platform API

One reference implementation uses its own service classes around the audit log (an audit service, a user lookup, an audit DAO wrapper). The services and lookups around the generated DAO, such as a UserDao helper, are application code, not platform API. Copy the pattern, not the names.

## Examples

### Variant seen in practice

- Shared audit service in the common services package, used by every custom operation of the application.
- The enumeration covers the domain events, for example user login, post published and organization created.
- The export operation stores its CSV through the file store service.

## Backend guidance

### Write the event from the operation that changes state

Interceptors run only for the platform's built-in operations (create, update, delete, list and so on). Custom operations get no interceptor, so each operation that changes state writes its own event. Put the write last, after the business change, inside the operation's transaction.

An operation call runs in one transaction. If the operation throws, all its writes roll back, including writes made before the throw. A stateful operation commits its writes when it returns without a fault. A non-stateful operation, or one that returns a modeled fault, rolls them back.

- Inject one event data-access object (DAO) with a reference, and call its create method from each operation.
- Build the event with the type, the message, the current time and the two associations (affected entity and acting user).
- Resolve the acting user from the security context once, in a shared helper, not in each operation.

### Keep the event immutable

The entity has no generated update or delete. Correct a wrong event by writing a new one, not by editing it.

The `immutable` flag is defined only on transfer operations, not on entities, so the model cannot mark the entity itself as immutable. Keep the event immutable by leaving update and delete operations out of the entity's operations.

### Do not swallow a failed event write

Unlike an audit row, a domain event is part of the business record: the timeline is wrong if it is missing. Let the write fail with the operation, so the transaction rolls back. If the event must not break the operation, wrap the write as in [[safe-failure-pattern]] and log the cause.

### Errors in the write

A failure to create the event is a platform failure, not a business rule. Do not throw a business fault for it. A modeled fault cannot be thrown from an interceptor; if an interceptor must report a business error, it throws only `InterceptorCallBusinessException`, which the platform turns into a 422 business error.

## Examples

### Variant seen in practice

- Each product lifecycle operation (finalize, approve, revoke, create) creates one event at the end of the operation.
- The event type is chosen per operation. Draft-new-version is the only product operation that writes no event.
- Event messages are human-readable and carry the version number.
- The application's own data-access wrappers and helper classes are application code. Copy the pattern, not the names.

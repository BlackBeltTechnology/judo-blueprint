## Backend guidance

### Write the event from the operation that changes state

Interceptors run only for built-in operations. Custom operations get no interceptor, so each operation that changes state writes its own event. Put the write last, after the business change, inside the operation's transaction.

- Inject one event data-access service with a reference, and call its create method from each operation.
- Build the event with the type, the message, the current time and the two associations (affected entity and acting user).
- Resolve the acting user from the security context once, in a shared helper, not in each operation.

### Keep the event immutable

The entity has no generated update or delete. Correct a wrong event by writing a new one, not by editing it.

### Do not swallow a failed event write

Unlike an audit row, a domain event is part of the business record: the timeline is wrong if it is missing. Let the write fail with the operation, so the transaction rolls back. If the event must not break the operation, wrap the write as in [[safe-failure-pattern]] and log the cause.

### Errors in the write

A failure to create the event is a platform failure, not a business rule. Do not throw a business fault for it. An interceptor, if one is used, throws only `InterceptorCallBusinessException` (the business wrapper used by interceptors).

## Examples

### alba

- Each product lifecycle operation (finalize, approve, revoke, create) creates one event at the end of the operation.
- The event type is chosen per operation. Draft-new-version is the only product operation that writes no event.
- Event messages are human-readable and carry the version number.
- The project's own data-access and helper classes are project code. Copy the pattern, not the names.

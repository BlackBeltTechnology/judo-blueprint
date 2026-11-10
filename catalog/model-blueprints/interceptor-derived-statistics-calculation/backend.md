## Backend guidance

### Attach the interceptor to built-in operations only

Register the interceptor, in `getOperations`, for the built-in list and refresh operations of the statistics transfer object. The platform never runs interceptors around custom, MAPPED or script operations, whatever `getOperations` returns. Do not expect it to run for a custom operation that returns the same data. If a custom operation needs the counts, it must compute them in its own body.

```java
@Override
public Object postCall(EOperation op, Object paramPayload, Object returnPayload)
        throws InterceptorCallBusinessException {
    if (returnPayload instanceof Payload single) {
        single.put("activeAccounts", countActiveAccounts(clock));
    }
    return OperationCallInterceptor.super.postCall(op, paramPayload, returnPayload);
}
```

The postCall hook returns the (possibly modified) payload; that return value becomes the result. Calling the super method at the end is project style; the platform default simply returns the payload.

### Throw only the interceptor exception

If the count fails, throw `InterceptorCallBusinessException`, the only business exception an interceptor may throw. Pass the FQN of a modeled fault transfer object as its type and put the message in the details (never null). A generated fault exception is checked and cannot be thrown from an interceptor, and a raw `RuntimeException` reaches the client as a generic 500.

### Compute the threshold from an injected clock

Project practice: build the date threshold once per call from a clock that the interceptor receives (the `clock` and the count helper in the sample are example project code). Tests can then fix the time; one shared clock with a test override is described in [[injectable-business-clock]].

```java
LocalDateTime threshold = LocalDateTime.now(clock).minusDays(ACTIVE_DAYS);
```

### Handle both payload shapes

A list returns a collection of payloads, a refresh returns one payload. Handle both, and read the identifier from the payload when a per-parent count is needed.

### Keep the count query cheap

Each call runs the count again. Filter on indexed columns, and keep the number of counted entities small. If the count is slow, switch to a stored value updated by a job. An entity-level stored value is also the choice when the value must be filterable or sortable at the DAO layer, which a transient attribute is not.

## Examples

### mlszksz-platform

- One interceptor is attached to the built-in list and refresh operations of the statistics transfer objects, both global and per-organization.
- The postCall hook counts users, news, offers, requests and announcements created or active in the last 30 days, and puts the counts into the payload.
- For per-organization statistics the hook reads the organization identifier from the payload and counts the users under it.
- The data-access services are generated SDK services for the entities, reached by injected references. Their names are project-specific.

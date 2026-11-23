## Interceptor scope

An `OperationCallInterceptor` is dispatched only for built-in operations. Custom operations and script operations do not pass through it. For a custom operation that must be logged, the operation logs explicitly, before or after its business action.

## Implementation Pattern

### Interceptor class
- `@Component(property={"judo.model.name=<model-name>"})` binds it to the application's model.
- Implements `OperationCallInterceptor` from `hu.blackbelt.judo.runtime.core.dispatcher`.
- `getName()` returns an identifier used for logging.

### Operation scoping
1. **All built-in operations:** do not override `getOperations()`. The interceptor receives every built-in operation call.
2. **Named built-in operations:** override `getOperations(AsmModel)` to return the `EOperation` instances resolved with `asmUtils.resolveOperation("FQN#operationName")`. Resolve them once and cache them. Listing a custom operation here has no effect.

### preCall hook
- Receives the `EOperation` and the parameter payload.
- Gets the fully qualified name with `AsmUtils.getOperationFQName(operation)`.
- Logs it at INFO level and returns the payload with `OperationCallInterceptor.super.preCall(operation, parameterPayload)`.

### postCall hook (optional)
- Logs the response, the elapsed time or the error status.
- When several interceptors are registered, their `preCall` and `postCall` hooks all run in registration order (`postCall` is not reversed).

**Exceptions:** an interceptor may throw only `InterceptorCallBusinessException`. Wrap any other failure in it. Project error helpers are not platform API.

### Key imports
- `hu.blackbelt.judo.meta.asm.runtime.AsmModel` and `AsmUtils`: resolving and naming operations.
- `hu.blackbelt.judo.runtime.core.dispatcher.OperationCallInterceptor`: the interface.
- `org.eclipse.emf.ecore.EOperation`: the EMF operation type.

## Custom operations

Write the log line inside the custom operation itself. Example project code (not platform API):

```java
log.info("OPERATION {} called by {}", "Order#confirm", currentUser);
```

## Examples

### Example
- Pattern: interceptor without a `getOperations()` override, so it logs every built-in operation call. The commented-out `getOperations()` shows the named-operation variant using `asmUtils.resolveOperation("[MODEL].[PACKAGE...].[TRANSFER]#[OPERATION]")` with lazy initialization.
- Notable: `@Component(property={"judo.model.name=<model-name>"})` binds the model. `preCall()` logs at INFO with a marker that makes the lines easy to grep. Custom operations of the project are not in this log.
- DI wiring: no `@Reference` dependencies. OSGi DS registers it when the bundle is active.

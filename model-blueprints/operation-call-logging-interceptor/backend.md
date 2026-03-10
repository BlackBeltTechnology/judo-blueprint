## Overview

Implements a global `OperationCallInterceptor` that logs the fully qualified name of every intercepted operation call in its `preCall()` hook. Serves as a development debugging tool and a template for building more sophisticated operation-level audit logging.

## Implementation Pattern

**Interceptor class:**
- `@Component(property={"judo.model.name=<model-name>"})` -- binds to the application's model
- Implements `OperationCallInterceptor` interface from `hu.blackbelt.judo.runtime.core.dispatcher`
- `getName()` returns the class simple name (used for logging/identification)

**Operation scoping (two variants):**
1. **Global (all operations):** Do not override `getOperations()` -- the interceptor receives all operation calls
2. **Targeted (specific operations):** Override `getOperations(AsmModel)` to return a collection of specific `EOperation` instances resolved via `asmUtils.resolveOperation("FQN#operationName")`. Cache the resolved operations for performance.

**preCall hook:**
- Receives the `EOperation` and the parameter payload
- Extracts the fully qualified operation name via `AsmUtils.getOperationFQName(operation)`
- Logs the operation name at INFO level
- Returns `OperationCallInterceptor.super.preCall(operation, parameterPayload)` to pass through without modification

**postCall hook (optional extension):**
- Can be overridden to log response details, execution time, or error status
- Useful for building an operation-level audit trail

**Key imports:**
- `hu.blackbelt.judo.meta.asm.runtime.AsmModel` and `AsmUtils` -- for resolving and naming operations
- `hu.blackbelt.judo.runtime.core.dispatcher.OperationCallInterceptor` -- the interceptor interface
- `org.eclipse.emf.ecore.EOperation` -- the EMF operation metadata type

## Examples

### rackinspect
- Key files: `interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/LogOperationCallInterceptor.java`
- Pattern: Global interceptor (no `getOperations()` override) that logs every operation call. The commented-out `getOperations()` code shows the targeted variant pattern with `asmUtils.resolveOperation("[MODEL].[PACKAGE...].[TRANSFER]#[OPERATION]")` and lazy initialization.
- Notable: Uses `@Component(property={"judo.model.name=rackinspect"})` for model binding. The `preCall()` logs at INFO level with visual markers for easy grep-ability in log output. Demonstrates both global and targeted scoping patterns in a single file (active vs commented).
- DI wiring: No `@Reference` dependencies -- pure interceptor with no service calls. Registered automatically by OSGi DS when the bundle is active.

---
id: "interceptor-global-logging"
title: "Global Operation Logging Interceptor"
domain: "backend"
category: "interceptor"
score: 78.7
usage_count: 10
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - alba
  - mlszksz-platform
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

A global pre-call interceptor that logs every intercepted operation's fully qualified name. By not overriding `getOperations()`, it applies to ALL operations. Useful for debugging and understanding operation dispatch flow during development. Typically shipped commented-out and enabled on demand.

## Structure

```java
@Component(property = { "judo.model.name=appname" })
public class InterceptorOperationLogger implements OperationCallInterceptor {

    private static final Logger log = LoggerFactory.getLogger(InterceptorOperationLogger.class);

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        String operationFQName = AsmUtils.getOperationFQName(operation);
        log.info("INTERCEPTED OPERATION: {}", operationFQName);
        return OperationCallInterceptor.super.preCall(operation, parameterPayload);
    }
}
```

Key: No `getOperations()` override means it intercepts ALL operations globally.

## Examples

### Trivia
`InterceptorOperationLogger` registered with `judo.model.name=trivia`. Logic is currently commented out but shows the pattern: `AsmUtils.getOperationFQName(operation)` to get the FQN, then log it. Acts as a development debugging aid.

### RackInspect
`LogOperationCallInterceptor` registered with `judo.model.name=rackinspect`. Implements both `preCall` (logs operation name + parameters) and `postCall` (logs return value). Same global logging approach, with `getOperations` commented out to intercept all operations.

### ALBA
`InterceptorOperationLogger` registered with `judo.model.name=Alba`. Logs with visual markers: `*** INTERCEPTED OPERATION ***` plus the operation FQN. Active (not commented out), providing runtime visibility into all operation calls across the system.

### mlszksz-platform
`LogOperationCallInterceptor` registered with `judo.model.name=MLSZKSZPlatform`. Currently disabled (getOperations commented out). Uses visual markers in log output. Demonstrates the pattern as a toggle-able debugging tool across the 65+ custom operations in the platform.

### judo-demo-miniworkflow
`LogInterceptor` registered with `judo.model.name=MiniWorkflow`. Active preCall implementation using emoji visual markers (`*** arrow-down INTERCEPTED OPERATION arrow-down ***`). Logs the operation FQN (e.g., `MiniWorkflow::DocumentTransfer.accept`). No `getOperations()` override, intercepting all 10 workflow operations globally.

### Ubives
`LogAuthenticationInterceptor` uses `AuthenticationInterceptor` interface (not `OperationCallInterceptor`) to log authentication events. Logs operation FQN, claim, realm, client, and all authentication attributes with formatted key-value pairs. Registered with `judo.model.name=Alba` (legacy model name). `isSuitableForOperation()` returns true for all operations. Variant of the pattern applied to authentication interception rather than operation interception.

### ParkHere
`LogOperationCallInterceptor` registered with `judo.model.name=ParkHere`. Implements `preCall` with visual markers logging the operation FQN. `getOperations()` method is commented out, serving as a toggle-able debugging tool. Can be enabled by uncommenting `getOperations()` to return all operations from the model.

### judo-partner
`LogOperationCallInterceptor` registered with `judo.model.name=Partner`. Logs all intercepted operation names with visual markers at INFO level. `getOperations()` is commented out, so it intercepts ALL operations globally. Serves as a debugging tool for the partner management system.

### workflow-poc
Both `LogOperationCallInterceptor` and `LogAuthenticationInterceptor` exist as `.java.default` templates (not activated). `LogOperationCallInterceptor` logs operation FQN via SLF4J. `LogAuthenticationInterceptor` logs operation FQN, claim, realm, client, and all authentication attributes. Both registered with `judo.model.name=workflow`. Would need renaming to `.java` and `.generator-ignore` entry to activate.

### ReserveApp
`InterceptorOperationLogger` registered with `judo.model.name=ReserveApp`. Active preCall logging with emoji arrow visual markers. Logs the operation FQN using `AsmUtils.getOperationFQName(operation)`. No `getOperations()` override, intercepting all operations globally. One of only two hand-written Java classes in the entire project.

## Trade-offs

- Pros: Zero-config debugging tool, shows full operation dispatch flow, trivial to enable/disable
- Cons: Performance overhead if left enabled in production (intercepts ALL operations), no filtering capability
- Alternative: Targeted interceptor with `getOperations()` for specific operations only

## Related Patterns

- interceptor-security-filter-validation
- interceptor-template-postcall
- interceptor-crud-lifecycle

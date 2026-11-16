---
id: interceptor-global-logging
title: Global Operation Logging Interceptor
description: "A global operation-call interceptor with no getOperations override that logs the fully qualified name of every built-in operation in preCall, shipped as a development aid and toggled by enabling or disabling the component; also the authentication variant."
aliases: ["operation logger", "debug interceptor", "LogOperationCallInterceptor"]
keywords: ["interceptor", "logging", "debug", "getOperations", "preCall", "AsmUtils", "operation FQN", "AuthenticationInterceptor"]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:judo-partner", "project:workflow-poc", "project:reserve-app", "status:established"]
category: interceptor
status: established
projects: [trivia, rackinspect, alba, mlszksz-platform, judo-demo-miniworkflow, ubives, park-here, judo-partner, workflow-poc, reserve-app]
evidence: ["trivia:unrecorded", "rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/LogOperationCallInterceptor.java", "alba:unrecorded", "mlszksz-platform:application/interceptors/src/main/java/hu/blackbelt/mlszksz/platform/interceptors/LogAuthenticationInterceptor.java", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "reserve-app:unrecorded"]
alternatives: []
related: [interceptor-security-filter-validation, interceptor-template-postcall, interceptor-crud-lifecycle, keycloak-jit-user-provisioning]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

During development you want to see which operations the runtime dispatches and in which order, with their names in the exact form `getOperations` expects. A tiny global interceptor logs the fully qualified name of each intercepted operation.

## Practice

### Platform: what "global" covers

- A `getOperations` that returns the default empty collection registers the interceptor for **all built-in operations**: create, update, delete, list, refresh, reference operations, range, template, metadata, principal, upload token, export and validate ([contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)).
- It never sees custom (SDK-implemented), mapped or script operations, even though the Javadoc says "all operation calls". A log that lacks your custom operation is normal ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- `AsmUtils.getOperationFQName(operation)` gives the name; the same string format is used to register targeted interceptors ([FQN reference](../../agent-docs/backend/interceptors.md#operation-fqn-format-reference)). The component needs `judo.model.name=<model>` ([registration](../../agent-docs/backend/interceptors.md#interceptor-component-registration)); the platform guide shows this logger as its first example ([example 1](../../agent-docs/backend/interceptors.md#example-1-simple-logging-interceptor)).
- The generator emits `Log*Interceptor.java.default` templates. They are not compiled until renamed to `.java`, and the renamed file needs no `.generator-ignore` entry ([.default templates](../../agent-docs/backend/interceptors.md#using-default-template-files)).

### Practice notes: one logger class, switched on only when needed

```java
// Example code
@Component(property = { "judo.model.name=<model>" })
public class InterceptorOperationLogger implements OperationCallInterceptor {

    private static final Logger log = LoggerFactory.getLogger(InterceptorOperationLogger.class);

    @Override public String getName() { return getClass().getSimpleName(); }

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        log.info("INTERCEPTED OPERATION: {}", AsmUtils.getOperationFQName(operation));
        return OperationCallInterceptor.super.preCall(operation, parameterPayload);
    }
}
```

- Many applications carry this class. Some keep it active, most ship it disabled (logic commented out, or the unrenamed `.java.default` template) and enable it on demand.
- Log at a level you can filter; the logger runs on every intercepted call, so leave it off in production or limit the log level.
- Variants seen: also log the parameter payload in `preCall` and the return value in `postCall`; and an `AuthenticationInterceptor` twin that logs the claim, realm, client and all token attributes for debugging token mapping ([authentication interceptor](../../agent-docs/backend/authentication-guide.md#authenticationinterceptor-interface), [[keycloak-jit-user-provisioning]]).
- Do not log payloads that contain personal data or secrets, and do not log the full token attributes outside development.

## Rationale

- It needs no configuration and shows the real dispatch flow, including the exact operation names for targeted interceptors.
- Cost: overhead on every call if left on, and no filtering. To look at a few operations only, return them from `getOperations`.

## Example

Developer needs the FQN of the update operation of an entity to register a targeted interceptor. The logger is enabled, the screen action is performed once, and the log line `INTERCEPTED OPERATION: <model>.services...#_updateInstance...` is copied into the targeted interceptor's `getOperations`. The logger is then disabled again.

## When to avoid

- In production at INFO level: it adds log volume and time on every call.
- To audit who did what: log lines are not an audit trail; see [[audit-event-trail]].
- To trace custom operations: they are not intercepted; log inside the operation.

## Related

- [[interceptor-security-filter-validation]] — a targeted pre-call interceptor
- [[interceptor-template-postcall]] — a targeted post-call interceptor
- [[interceptor-crud-lifecycle]] — interceptors that change behaviour
- [[keycloak-jit-user-provisioning]] — authentication interceptors
- [[audit-event-trail]] — the real audit trail

---
id: "interceptor-template-postcall"
title: "Post-Call Interceptor for Data Stripping/Modification"
domain: "backend"
category: "interceptor"
score: 59.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - park-here
---
## Description

A post-call interceptor that modifies the return payload of an operation to strip sensitive data or modify fields before the response reaches the client. The interceptor targets specific operations (e.g., template retrieval, refresh), casts the return payload to `Payload`, and removes or modifies specific fields. This prevents internal configuration data, user lists, or other sensitive information from leaking to the frontend.

## Structure

```java
@Component(property = { "judo.model.name=appname" })
public class TemplateInterceptor implements OperationCallInterceptor {

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        // Target specific operation
        return List.of(asmUtils.resolveOperation(
            "app.services.Entity#_getTemplateEntity"
        ).orElseThrow());
    }

    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
        Payload payload = (Payload) returnPayload;
        // Strip sensitive data from nested collections
        Collection<Payload> items = payload.getAsCollectionPayload("nestedRelation");
        if (items != null) {
            for (Payload item : items) {
                item.remove("sensitiveField");
                item.remove("internalConfig");
            }
        }
        return returnPayload;
    }
}
```

## Examples

### Trivia
`TemplateInterceptor` with all logic commented out. Demonstrates: targeting `_refreshInstance` operations, injecting `TestDao`, extracting UUID from `Payload.getAs(UUID.class, "__identifier")`, and modifying Test status in `postCall()`. Serves as copy-paste reference for new interceptors.

### ParkHere
`UserSettingsTemplateInterceptor` targets `UserSettings#_getTemplateUserSettings`. In postCall, iterates `accessedParkingGarages` collection payload and removes `emailTemplateOfTheGarage` (internal template config), `accessedUsers` (user list), and `isActive` (status flag). Prevents leaking internal garage configuration and user data to the frontend user settings page.

## Trade-offs

- Pros: Prevents data leakage, operates transparently without changing operation logic, targets specific operations
- Cons: Payload manipulation is not type-safe, field names are hardcoded strings, removed data cannot be recovered downstream
- Alternative: Model-level field exclusion, separate transfer objects with restricted fields, mask-based projection

## Related Patterns

- interceptor-global-logging
- interceptor-security-filter-validation
- interceptor-crud-lifecycle

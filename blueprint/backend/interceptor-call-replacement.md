---
id: "interceptor-call-replacement"
title: "Interceptor Call Replacement via ignoreDecoratedCall"
domain: "backend"
category: "interceptor"
score: 12.3
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - alba
---
## Description

An interceptor pattern where `ignoreDecoratedCall()` returns `true`, causing the original (decorated) operation to be completely skipped. The interceptor's `preCall()` method provides the replacement implementation. This effectively allows an interceptor to replace a generated operation entirely without modifying generated code, useful when the generated CRUD operation is insufficient and a completely different entity needs to be created instead.

## Structure

```java
@Component(property = { "judo.model.name=AppName" })
public class EntityCreateInterceptor implements OperationCallInterceptor {

    @Reference AlternateEntityDao alternateDao;

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        return Stream.of("App.services.Service#_createInstanceTarget")
            .map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
    }

    @Override
    public boolean ignoreDecoratedCall() {
        return true;  // Skip the original operation entirely
    }

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        if (parameterPayload instanceof CreateInstanceCall.CreateInstanceCallPayload payload) {
            SourceProfile profile = SourceProfile.from(payload.getInput());

            // Create a DIFFERENT entity than what the operation would have created
            AlternateEntityForCreate create = AlternateEntityForCreate.builder()
                .withEmail(profile.getEmail())
                .withStatus(profile.getStatus())
                .build();
            alternateDao.create(create);

            return payload;
        }
        return OperationCallInterceptor.super.postCall(operation, parameterPayload, null);
    }
}
```

Key: `ignoreDecoratedCall() = true` prevents the original operation from executing.

## Examples

### ALBA
`AdminUserCreateInterceptor` intercepts `_createInstanceAdminProfiles`. Instead of creating an AdminProfile entity (the default behavior), it extracts profile data and creates a `UserTransfer` entity that bridges admin profiles to the main user system. Optional fields (firstName, lastName, shortIntro, role, profilePicture) are handled with null-safe checks. Institution relation is set if provided.

## Trade-offs

- Pros: Completely replaces generated behavior without code modification, allows entity type bridging, clean interception pattern
- Cons: Original operation is silently suppressed (can be confusing to debug), interceptor must handle all aspects of the replaced operation, return value may not match caller expectations
- Alternative: Custom operation that wraps or overrides the generated operation, or model-level customization of the create behavior

## Related Patterns

- interceptor-crud-lifecycle
- interceptor-global-logging
- custom-operation-osgi-component

---
id: "interceptor-security-filter-validation"
title: "Security Filter Validation Interceptor"
domain: "backend"
category: "interceptor"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

A targeted pre-call interceptor that validates the query filter on list operations to prevent unauthorized data access. It intercepts specific list operations and validates that the filter matches an expected regex pattern (e.g., only allowing queries by specific UUID). This prevents enumeration attacks and unauthorized bulk data access.

## Structure

```java
@Component(property = { "judo.model.name=appname" })
public class ListInterceptor implements OperationCallInterceptor {

    private AsmUtils asmUtils;
    private List<EOperation> interceptedOperations;

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (interceptedOperations == null) {
            if (asmUtils == null) {
                asmUtils = new AsmUtils(asmModel.getResourceSet());
            }
            interceptedOperations = Stream.of(
                "app.actors.player.Player#_listTests"
            ).map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
        }
        return interceptedOperations;
    }

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        ListCallPayload<UUID> payload = (ListCallPayload<UUID>) parameterPayload;
        String filter = payload.getQueryCustomizer().getFilter();
        if (!filter.matches("^this\\.id==\"[0-9a-f-]*\"$")) {
            throw new RuntimeException("Unauthorized query pattern");
        }
        return OperationCallInterceptor.super.preCall(operation, parameterPayload);
    }
}
```

Key elements: lazy `AsmUtils` initialization, `ListCallPayload` casting, regex validation on filter string.

## Examples

### Trivia
`ListInterceptor` targets `trivia.actors.player.Player#_listTests` only. Validates filter matches `^this\.id==\"[0-9a-f-]*\"$` (UUID-only queries). Prevents players from listing all tests or using wildcard filters. Throws RuntimeException on violation.

## Trade-offs

- Pros: Prevents data enumeration, enforces query-level security, targeted to specific operations
- Cons: Regex-based validation is brittle, throws raw RuntimeException (should use typed error), hardcoded operation FQN
- Alternative: Model-level access control via JUDO access expressions, or `VariableResolver`-based actor scoping

## Related Patterns

- interceptor-global-logging
- interceptor-template-postcall

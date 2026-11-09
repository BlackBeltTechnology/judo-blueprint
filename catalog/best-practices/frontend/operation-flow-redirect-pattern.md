---
id: "operation-flow-redirect-pattern"
title: "Operation Flow Redirect via Generator Override and OperationFlowManager"
domain: "frontend"
category: "navigation"
score: 43.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - workflow-poc
---
## Description

Implement dynamic post-operation navigation by combining a Handlebars generator template override with a custom `OperationFlowManager` service. Operations annotated with `@redirect` in the ESM model return transfer objects containing navigation metadata (actor, access, record identifiers, or further operations). A generator override fragment intercepts these outputs and routes them through a `processRedirect()` call, while the `OperationFlowManager` (registered as a Pandino service) interprets the redirect payload to navigate the user to the appropriate page or trigger a subsequent operation. This enables multi-step workflow flows where each operation can dynamically determine the next screen.

## Structure

Three coordinated pieces:

1. **Transfer objects** carry redirect metadata:
```
TransferObject UpdateRedirect { actor, access, idName, idValue }
TransferObject CreateRedirect { actor, access, operation }
```

2. **Handlebars generator override** (`operation-primary-output-handler.fragment.hbs`):
```handlebars
{{# if operation.output }}
    {{# if (elementHasAnnotation operation.output.target 'redirect') }}
        if (result) {
            setIsLoading(false);
            await processRedirect(result
            {{# unless action.actionDefinition.isParameterlessCallOperationAction }}
                , async () => await onSubmit(result)
            {{/ unless }}
            );
        } else
    {{/ if }}
{{/ if }}
```

3. **OperationFlowManager** in `application-customizer.tsx`:
```typescript
const operationFlowManager: OperationFlowManager = {
  handleResult: (input) => {
    const { actor, access, idName, idValue, operation } = input as any;
    if (idName && idValue) {
      return { filterRecords: { [idName]: [{ operator: 'equal', value: idValue }] }, access, actor };
    }
    if (operation) {
      return { operation, access, actor };
    }
    return { access, actor };
  },
};
```

File locations:
```
generator-overrides/ui-react/actor/src/fragments/operations/
  operation-primary-output-handler.fragment.hbs
src/custom/application-customizer.tsx  (.generator-ignore protected)
```

## Examples

### workflow-poc
Workflow operations (`startWorkflow`, `navigate`, `execute`, `assign`) return `CreateRedirect` or `UpdateRedirect` objects annotated with `@redirect`. The HBS fragment intercepts these in generated code and calls `processRedirect()`. The OperationFlowManager routes to specific records (via `filterRecords` with `idName`/`idValue`) or triggers follow-up operations. This enables a multi-step task management flow without any individual hook overrides.

## Trade-offs

- **Pros**: Enables dynamic multi-step navigation from backend-driven operation results; single generator override applies to all annotated operations; no need to override hooks per-page; clean separation of redirect logic
- **Cons**: Requires Handlebars template knowledge; tightly couples frontend to backend redirect contract; generator override is fragile if framework changes template structure; debugging redirect flow is harder than simple navigation
- **When to use**: Workflow or multi-step operation systems where the backend determines the next UI step after an operation completes

## Related Patterns

- [post-operation-navigation-hook](post-operation-navigation-hook.md)
- [handlebars-generator-template-override](handlebars-generator-template-override.md)
- [application-customizer-hub](application-customizer-hub.md)

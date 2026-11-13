## Overview

The template layer is validated by application code. The platform's interceptors run only on built-in create, update and delete operations, so a rule about template structure goes on the built-in operation it protects. A custom operation that returns template parameters is application code and never triggers an interceptor.

## Implementation Pattern

- **Built-in create and update.** Put structure checks in the interceptor's `preCall` for the built-in operation on the template. Check that at least one group exists. Throw only `InterceptorCallBusinessException` for a business failure; the dispatcher turns it into the modeled fault's 422 response.
- **Name generation.** When the name is blank, a `postCall` may fill it in. `postCall` runs in registration order, the same as `preCall` (not reversed), so register it before any other interceptor that reads the name.
- **Group and parameter consistency.** Check that the parameter set matches the template type on the built-in group update, not on a custom operation.
- **Validation helper (application code).** Checks shared by several interceptors go in an application service, for example a `DimensionService`. The service is not part of the platform.
- **Template lookup (custom operation).** A custom operation returns the template's group hierarchy for a dynamic form. Custom operations never run interceptors, so do not put validation there.

```java
@Component(property = { "judo.model.name=<model>" })
public class DimensionTemplateCreateInterceptor implements OperationCallInterceptor {
    @Override
    public Object preCall(EOperation operation, Object parameterPayload) throws InterceptorCallBusinessException {
        if (isTemplateCreate(operation) && !hasGroups(parameterPayload)) {
            throw new InterceptorCallBusinessException(
                    "<app>.services.TemplateNeedsGroup", "TEMPLATE_NEEDS_GROUP",
                    Map.of("message", "A template needs at least one group"), null, null);
        }
        return parameterPayload;
    }
    // getName(), postCall(...) and the helper methods are omitted
}
```

The interceptor class is application code that implements the platform's `OperationCallInterceptor`. Its `preCall` and `postCall` receive the operation and a payload, and may throw only `InterceptorCallBusinessException`, whose type is the fully qualified name of a modeled fault; a modeled fault's own generated exception cannot be thrown here ([interceptors guide](../../agent-docs/backend/interceptors.md), Throwing a Business Error from an Interceptor). The exception rolls back the whole operation. The check itself and the helpers are application code.

## Examples

### Variant seen in practice
- Key files: the create and update interceptors of the template, the update interceptor of the template group, the custom template-parameters operation and the shared service.
- Pattern: interceptors on built-in create and update check that a template has at least one group, and the group update checks the template type. An application service holds the shared checks. A custom operation returns the template parameters for a dynamic form.
- Notable: the template name is generated in `postCall` when left blank; the group checks differ for the two template types, and `AppI18n` provides the localized messages. The initial templates are seeded from a spreadsheet during setup.

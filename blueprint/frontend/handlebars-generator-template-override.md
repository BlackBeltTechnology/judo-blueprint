---
id: "handlebars-generator-template-override"
title: "Handlebars Generator Template Override for Cross-Cutting Frontend Logic"
domain: "frontend"
category: "build"
score: 18.8
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - workflow-poc
---
## Description

Override specific Handlebars template fragments used by the JUDO code generator to inject custom logic into all generated frontend components that match a pattern. Unlike `.generator-ignore` (which protects individual files from regeneration) or hook overrides (which customize individual page behavior at runtime), HBS template overrides modify the generator's output templates themselves, causing the custom logic to appear in every generated file that uses the overridden fragment. This is the most powerful cross-cutting customization mechanism, affecting all generated code that includes the fragment.

## Structure

```
application/frontend-react/
  generator-overrides/
    ui-react/
      actor/
        src/
          fragments/
            operations/
              operation-primary-output-handler.fragment.hbs   # Override for operation output handling
            some-other/
              custom-fragment.fragment.hbs                    # Override for other patterns
```

The override file must exactly match the path structure expected by the generator. The generator checks `generator-overrides/` before using its built-in templates.

Fragment files use Handlebars syntax with access to the ESM model:
```handlebars
{{# if (elementHasAnnotation operation.output.target 'redirect') }}
    // Custom code injected into all operations with @redirect annotation
    await processRedirect(result);
{{/ if }}
```

Key Handlebars helpers available:
- `elementHasAnnotation` - check for ESM annotations
- `operation.output.target` - access operation output type info
- `action.actionDefinition.isParameterlessCallOperationAction` - check action properties

## Examples

### workflow-poc
Overrides `operation-primary-output-handler.fragment.hbs` to intercept operation outputs annotated with `@redirect`. The override injects `processRedirect(result)` calls into all generated operation handlers where the output target has the annotation. This causes every workflow operation (startWorkflow, navigate, execute, assign) to route through the custom OperationFlowManager instead of the default output dialog.

## Trade-offs

- **Pros**: Single override affects all generated components; no per-page hook code needed; annotation-driven (only affects annotated operations); survives regeneration
- **Cons**: Requires deep knowledge of generator internals and Handlebars template structure; fragile if framework updates the template; hard to debug (generated output must be inspected); risk of breaking all generated pages if template is incorrect
- **When to use**: When a cross-cutting concern (redirect handling, custom output processing, authentication flow) needs to be injected into many generated components based on model annotations

## Related Patterns

- [operation-flow-redirect-pattern](operation-flow-redirect-pattern.md)
- [generator-override-extra-dependencies](generator-override-extra-dependencies.md)
- [generator-ignore-app-theme](generator-ignore-app-theme.md)
- [flutter-generator-template-override](flutter-generator-template-override.md)

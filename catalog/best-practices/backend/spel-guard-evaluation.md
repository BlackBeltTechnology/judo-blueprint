---
id: "spel-guard-evaluation"
title: "SpEL-Based Guard Expression Evaluation"
domain: "backend"
category: "service"
score: 43.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - workflow-poc
---
## Description

A pattern for evaluating dynamic boolean expressions at runtime using Spring Expression Language (SpEL). Guard conditions are stored as strings on entities (e.g., workflow transitions) and evaluated against a dynamic context. A custom `PropertyAccessor` resolves named variables from entity attributes, allowing conditions like `isApproved == true` without compiled code. The pattern handles missing properties gracefully by returning `false` for unknown variables.

## Structure

```java
// Custom PropertyAccessor resolves entity attributes as SpEL variables
class ContextVariableResolver implements PropertyAccessor {
    private final Map<String, Object> variables;

    public ContextVariableResolver(Context context, ContextDao contextDao) {
        this.variables = new HashMap<>();
        contextDao.queryAttributes(context).selectList().forEach(attr -> {
            Object value = switch (attr.getType()) {
                case BOOLEAN -> Boolean.valueOf(attr.getValue());
                case STRING  -> String.valueOf(attr.getValue());
                case NUMERIC -> Long.valueOf(attr.getValue());
            };
            this.variables.put(attr.getName(), value);
        });
    }

    @Override
    public boolean canRead(EvaluationContext ctx, Object target, String name) {
        return variables.containsKey(name);
    }

    @Override
    public TypedValue read(EvaluationContext ctx, Object target, String name) {
        return new TypedValue(variables.get(name));
    }
}

// Evaluate guard expression
private boolean evalBoolExpression(Context context, String expr) {
    PropertyAccessor resolver = new ContextVariableResolver(context, contextDao);
    SpelExpressionParser parser = new SpelExpressionParser();
    StandardEvaluationContext evalContext = new StandardEvaluationContext();
    evalContext.addPropertyAccessor(resolver);

    try {
        return parser.parseExpression(expr).getValue(evalContext, Boolean.class);
    } catch (SpelEvaluationException e) {
        if (e.getMessageCode() == SpelMessage.PROPERTY_OR_FIELD_NOT_READABLE ||
            e.getMessageCode() == SpelMessage.PROPERTY_OR_FIELD_NOT_READABLE_ON_NULL) {
            return false;  // Missing property -> guard fails safely
        }
        throw e;
    }
}

// Evaluate all guards on a transition (AND logic)
private boolean evalGuards(Context context, Transition transition) {
    return transitionDao.queryGuards(transition).selectList().stream()
        .allMatch(guard -> evalBoolExpression(context, guard.getExpression()));
}
```

Key elements:
- `SpelExpressionParser` for parsing string expressions
- Custom `PropertyAccessor` for resolving domain-specific variables
- Typed value conversion (BOOLEAN, STRING, NUMERIC) from string attribute values
- Graceful handling of missing properties (returns `false`, no exception)
- All guards must pass (`allMatch`) for a transition to fire

## Examples

### workflow-poc
`WorkflowUtils.evalGuards()` evaluates guard expressions on workflow transitions. `WorkflowContextVariableResolver` loads context attributes from the database and exposes them as typed SpEL variables. Guards are stored as string expressions on `Guard` entities linked to transitions. Multiple guards on a transition are AND-combined via `allMatch()`. Missing or undefined attributes cause the guard to return `false`, preventing transitions when preconditions are not met. Used for both event-triggered and immediate (automatic) transitions.

## Trade-offs

- Pros: Dynamic rule evaluation without code changes, supports complex boolean logic, type-safe variable resolution, graceful handling of missing data
- Cons: SpEL expression errors are runtime failures, no compile-time validation of expressions, performance overhead for expression parsing, limited to boolean evaluation
- Alternative: Compiled Java predicates (type-safe but requires code changes), model-level constraints (tighter integration), JavaScript/Groovy evaluation (more flexible but heavier)

## Related Patterns

- state-lifecycle-operation
- safe-failure-pattern
- correlation-based-event-chaining

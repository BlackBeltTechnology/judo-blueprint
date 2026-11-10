---
id: spel-guard-evaluation
title: SpEL-Based Guard Expression Evaluation
description: "Guard conditions stored as strings on entities are evaluated at runtime with Spring Expression Language against a context-backed property accessor, and a missing variable makes the guard false."
aliases: [runtime guard expressions, SpEL guards, dynamic boolean rules]
keywords: [spel, spring expression language, guard, PropertyAccessor, workflow transition, runtime rule, expression]
tags: ["domain:backend", "layer:backend", "project:workflow-poc", "status:single-project"]
category: logic
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: []
related: [state-lifecycle-operation, safe-failure-pattern, correlation-based-event-chaining, token-based-workflow-execution]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

In a workflow engine the conditions on transitions are data, not code: an administrator or a YAML upload defines them, so they exist only at runtime. The engine stores each guard as a string, such as `isApproved == true`, and evaluates it with Spring Expression Language against the attributes of the current process context.

## Practice

### Platform base

- The agent-docs do not cover SpEL, and the platform's own expression languages (JQL in the model, JCL scripts in operation bodies) are compiled with the model and cannot be built from user-entered strings at runtime ([operation scripts](../../agent-docs/model/jcl-operation-scripts.md)). SpEL is a plain Java library used inside a custom operation or service; it is project practice, not a platform feature.
- The evaluator is ordinary Java in a service injected into the custom operations ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)). Guard and context rows are read through generated DAOs.
- Custom operations are not intercepted, so who may fire a transition is checked inside the operation, not by a guard expression alone ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- An exception thrown from the evaluator inside the operation propagates. To refuse a transition as a business error, map it to a fault that the operation declares ([modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)); a raw runtime exception becomes a generic 500.

### Project practice: context-backed property accessor

This layer is project practice (workflow-poc), not a platform feature:

- Store each guard as a string on a guard entity linked to the transition. A transition may have several guards; all must be true (`allMatch`).
- Load the context attributes (name, type, string value) from the database and convert them to typed values (boolean, string, number). Expose them to SpEL through a custom `PropertyAccessor`, so an expression refers to `isApproved` rather than a bean path.
- Evaluate with a `StandardEvaluationContext` holding only that accessor. Do not give user-written expressions access to arbitrary beans or types; a string that is evaluated is code.
- A missing variable is a normal state before the attribute has been set. Catch the SpEL "property not readable" errors and return `false`; rethrow every other SpEL error (syntax, type) so a broken expression is noticed ([[safe-failure-pattern]]).
- Validate expressions when they are saved (parse them), because there is no compile-time check.

```java
// Example project code: Context, ContextDao, Transition, TransitionDao are project/generated types
class ContextVariableResolver implements PropertyAccessor {
    private final Map<String, Object> variables = new HashMap<>();

    ContextVariableResolver(Context context, ContextDao contextDao) {
        contextDao.queryAttributes(context).selectList().forEach(attr -> {
            Object value = switch (attr.getType()) {
                case BOOLEAN -> Boolean.valueOf(attr.getValue());
                case STRING  -> String.valueOf(attr.getValue());
                case NUMERIC -> Long.valueOf(attr.getValue());
            };
            variables.put(attr.getName(), value);
        });
    }
    @Override public boolean canRead(EvaluationContext ctx, Object target, String name) {
        return variables.containsKey(name);
    }
    @Override public TypedValue read(EvaluationContext ctx, Object target, String name) {
        return new TypedValue(variables.get(name));
    }
    // getSpecificTargetClasses, canWrite, write omitted
}

private boolean evalBoolExpression(Context context, String expr) {
    StandardEvaluationContext evalContext = new StandardEvaluationContext();
    evalContext.addPropertyAccessor(new ContextVariableResolver(context, contextDao));
    try {
        return Boolean.TRUE.equals(new SpelExpressionParser().parseExpression(expr)
            .getValue(evalContext, Boolean.class));
    } catch (SpelEvaluationException e) {
        if (e.getMessageCode() == SpelMessage.PROPERTY_OR_FIELD_NOT_READABLE
            || e.getMessageCode() == SpelMessage.PROPERTY_OR_FIELD_NOT_READABLE_ON_NULL) {
            return false;   // missing attribute: guard fails safely
        }
        throw e;
    }
}

private boolean evalGuards(Context context, Transition transition) {
    return transitionDao.queryGuards(transition).selectList().stream()
        .allMatch(guard -> evalBoolExpression(context, guard.getExpression()));
}
```

## Rationale

- Rules change without a build, which is the point of a data-driven workflow.
- A restricted accessor keeps the vocabulary small and typed.
- Cost: expression errors are runtime failures, there is no compile-time check, and parsing has overhead (cache parsed expressions if guards are hot).

## Example

In workflow-poc `WorkflowUtils.evalGuards()` evaluates the guards of a transition. A context resolver loads the context attributes from the database as typed SpEL variables. Guards are string expressions on guard entities linked to transitions, and several guards are AND-combined. A missing attribute makes a guard false, so a transition does not fire until its preconditions exist. The same evaluation serves event-triggered and automatic transitions.

## When to avoid

- The rules are known at design time: write them as model expressions or Java predicates, which are validated at build time.
- Expressions come from untrusted users: SpEL is a full expression language, so restrict the evaluation context strictly or choose a smaller grammar.
- You need more than booleans: this pattern evaluates conditions only.

## Related

- [[state-lifecycle-operation]] — the state transitions the guards protect
- [[safe-failure-pattern]] — the narrow catch for missing variables
- [[correlation-based-event-chaining]] — chained events that trigger guarded transitions
- [[token-based-workflow-execution]] — the engine that evaluates the guards

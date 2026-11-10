---
id: correlation-based-event-chaining
title: Correlation-Based Event Chaining with ThreadLocal
description: "Events raised during one trigger share a correlation id (generated per request thread) and are processed one after another by querying the next unprocessed event of the same chain."
aliases: [event chain, correlation id, cascading events]
keywords: [correlation id, event chain, threadlocal, workflow, cascade, processed flag]
tags: ["domain:backend", "layer:backend", "project:workflow-poc", "status:single-project"]
category: operation
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A single external trigger can cause a transition whose actions raise further events, which cause further transitions. Persisting each event with a correlation id and a processed flag lets the engine drain the chain deterministically: process one event, mark it processed, then fetch the next unprocessed event of the same chain.

## Practice

### Platform base

- Events are ordinary entities created through the generated builder and DAO, and queried with typed filters (`StringFilter`, `BooleanFilter`) and ordering ([query patterns](../../agent-docs/backend/data-access-guide.md#query-patterns)). `selectOne()` returns an `Optional` ([query result methods](../../agent-docs/backend/data-access-guide.md#query-result-methods)).
- The whole operation, including all chained events, runs in one transaction; an exception rolls back every write made so far ([ordering and combining interceptors](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors) describes the transaction scope).
- The platform has its own request correlation, the `X-Exchange-Id` header ([Debugging and Monitoring Guide](../../agent-docs/backend/debugging-and-monitoring-guide.md)); it is for log tracing and is separate from the domain correlation id described here.
- Async interceptors and other threads run outside the transaction and without context variables ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)), so a ThreadLocal value is not visible there.

### Project practice: correlation id and recursive drain

This is workflow-poc project code, not a platform feature.

```java
// Example project code (workflow engine)
private static final ThreadLocal<String> correlationID =
    ThreadLocal.withInitial(() -> UUID.randomUUID().toString());

Event event = eventDao.create(EventForCreate.builder()
    .withEventID(input.getEventID())
    .withCorrelationID(correlationId)
    .build());

private void processEvent(Token token, Event event) {
    findAndExecuteTransition(token, event);
    event.setProcessed(true);
    eventDao.update(event);

    eventDao.query()
        .filterByCorrelationID(StringFilter.equalTo(getCorrelationID()))
        .filterByProcessed(BooleanFilter.isFalse())
        .orderBy(EventAttribute.SEQUENCE)
        .selectOne()
        .ifPresent(nextEvent -> processEvent(token, nextEvent));
}
```

- Events carry two ids: what happened (`eventID`) and which chain (`correlationID`). A sequence attribute gives a deterministic order inside a chain.
- If the caller supplies a correlation id, the event is only stored (another run processes the chain); otherwise it is processed immediately.
- Pass the correlation id explicitly to actions and nested calls ([[action-delegation-workflow]]) instead of relying on the ThreadLocal alone.
- A ThreadLocal is never cleared by itself: on a pooled request thread the same id would be reused by later requests. Remove it at the end of the outermost operation.
- Recursion has no cycle detection; cap the chain length or loop iteratively.
- Use one clock when ordering by timestamp ([time zones](../../agent-docs/backend/platform-behavior-reference.md#time-and-time-zones)).

## Rationale

- Cascading transitions are driven from a single trigger with a persistent log of every event, which also helps debugging ([[audit-event-trail]]).
- Cost: thread-bound state, deep recursion for long chains, and no protection against cycles.

## Example

In workflow-poc a trigger operation creates an event with the caller's or a generated correlation id. Processing finds the current state's transition for that event, executes it, marks the event processed and looks up the next unprocessed event with the same correlation id. Actions run during the transition (on enter, on leave, on transition) can create further events with the same id, so one trigger advances the workflow as far as it can go.

## When to avoid

- When processing must be asynchronous or distributed: use a queue and a saga.
- When there is a single transition per request: no chain is needed ([[state-lifecycle-operation]]).

## Related

- [[state-lifecycle-operation]] — simple single-step transitions
- [[audit-event-trail]] — persistent event rows as history
- [[action-delegation-workflow]] — actions that raise chained events
- [[token-based-workflow-execution]] — the engine this chain drives
- [[dao-fluent-query-filter]] — the queries used to fetch the next event

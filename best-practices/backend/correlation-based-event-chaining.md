---
id: "correlation-based-event-chaining"
title: "Correlation-Based Event Chaining with ThreadLocal"
domain: "backend"
category: "operation"
score: 43.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - workflow-poc
---
## Description

A pattern for chaining multiple events within a single logical operation using a correlation ID stored in a ThreadLocal. When an operation triggers an event that causes a state transition, the transition may fire actions that generate additional events. All events within the same trigger share a correlation ID, enabling sequential processing. After processing one event, the system queries for the next unprocessed event in the same correlation chain, creating a recursive processing loop.

## Structure

```java
// ThreadLocal correlation ID generator
private static final ThreadLocal<String> correlationID =
    ThreadLocal.withInitial(() -> UUID.randomUUID().toString());

public String getCorrelationID() {
    return correlationID.get();
}

// Create event with correlation ID
Event event = eventDao.create(EventForCreate.builder()
    .withEventID(input.getEventID())
    .withCorrelationID(correlationId)
    .build());

// Process event and check for chained events
private void processEvent(Token token, Event event) {
    // Find matching transition and execute
    findAndExecuteTransition(token, event);

    // Mark event as processed
    event.setProcessed(true);
    eventDao.update(event);

    // Check for next event in correlation chain
    eventDao.query()
        .filterByCorrelationID(StringFilter.equalTo(getCorrelationID()))
        .filterByProcessed(BooleanFilter.isFalse())
        .orderBy(EventAttribute.SEQUENCE)
        .selectOne()
        .ifPresent(nextEvent -> processEvent(token, nextEvent));
}
```

Key elements:
- `ThreadLocal<String>` ensures correlation ID is unique per request thread
- Events are persisted with both `eventID` (what happened) and `correlationID` (which chain)
- After processing, the system recursively checks for unprocessed events in the same chain
- Ordering by `SEQUENCE` ensures deterministic processing order
- Enables cascading state transitions from a single external trigger

## Examples

### workflow-poc
`TriggerCustomImplementation` creates an `Event` with either the caller-provided `correlationID` or a thread-local generated one. If no explicit correlation ID is provided, it processes the event immediately. `processEvent()` finds the current state's matching transition by `eventID`, executes the transition via `WorkflowUtils.step()`, marks the event as processed, then recursively calls `getNextEvent()` to find the next unprocessed event in the same correlation chain. Actions executed during transitions (ON_ENTER, ON_LEAVE, ON_TRANSITION) may create additional events with the same correlation ID, enabling cascading workflow advancement.

## Trade-offs

- Pros: Enables complex multi-step workflows from a single trigger, deterministic ordering, persistent event log for debugging, supports cascading transitions
- Cons: ThreadLocal can leak in thread-pool scenarios, recursive processing may cause deep stacks, no built-in cycle detection, correlation chain is tied to a single thread
- Alternative: Message queue-based event processing (async, scalable), saga pattern (distributed), in-memory state machine (no persistence overhead)

## Related Patterns

- state-lifecycle-operation
- audit-event-trail
- dao-fluent-query-filter

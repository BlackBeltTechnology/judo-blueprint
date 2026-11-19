---
id: safe-failure-pattern
title: Safe Failure Pattern for Non-Critical Operations
description: "Secondary work such as audit rows, statistics or notifications is wrapped so that its failure is logged but never breaks the primary operation, and loops over items continue after a single failure."
aliases: [swallow secondary errors, best-effort side effects]
keywords: [try catch, non-critical, audit, interceptor, scheduler, resilience, log and continue]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "project:workflow-poc", "status:emerging"]
category: error
status: emerging
projects: [mlszksz-platform, workflow-poc]
evidence: ["mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/AuditLogServiceImpl.java", "workflow-poc:unrecorded"]
alternatives: []
related: [audit-event-trail, quartz-scheduled-job, interceptor-aggregation-postcall, spel-guard-evaluation]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Some work is secondary: writing an audit row, updating statistics, sending a notification, cleaning up expired items. If it throws, the user should still get the result of the primary operation. The practice wraps such work in a narrow try/catch that logs and moves on, and does the same per item inside batch loops.

## Practice

### Platform base: what an exception costs you

- Synchronous interceptors run inside the operation's transaction. An exception from `preCall` or `postCall` rolls back the DAO write of the operation, including writes of earlier interceptors ([ordering and combining interceptors](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)). A secondary interceptor that must not break the write has to catch its own failures, except a failed database write: on PostgreSQL a caught DAO failure aborts the whole transaction, so the next statement fails. Let such a failure propagate so the operation rolls back, or move the write to an async interceptor.
- A raw `RuntimeException` leaving an interceptor is wrapped by the dispatcher as `InternalServerException` and the client sees a generic 500. A business refusal must be an `InterceptorCallBusinessException` ([throwing a business error from an interceptor](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).
- An async interceptor runs outside the transaction and its exceptions are lost, so it needs no catch for the transaction's sake, but should still log ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)).
- A custom operation runs in one transaction, so its DAO writes commit or roll back together when it throws ([custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations)). A call that joins an existing transaction is not rolled back by itself ([platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md#transaction-rollback)). A DAO exception the operation catches does not roll the call back by itself. On PostgreSQL the rest of the transaction then fails, while HSQLDB rolls back only the failed statement, so rethrow or return a fault to roll back reliably ([custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations)).

### Practice notes: log and continue

This layer is a convention built on the platform, not a platform feature:

- Catch only around the secondary action, never around the primary write. Catch `Exception`, log at warn or error with the cause, and do not rethrow.
- An interceptor `postCall` that does secondary work still returns the payload it received.
- In a loop over items, catch per item and continue, so one bad row does not stop the rest. Count successes and failures.
- Never swallow errors that mean the caller must know: business refusals, validation and authorisation failures stay exceptions.
- Narrow the catch when the failure has a known, harmless meaning (see the guard example below); rethrow everything else.

```java
// Example code: auditLogDao, log and service are generated members
public void log(ActionType type, String entityType, String entityId, Map<String, Object> details) {
    try {
        auditLogDao.create(auditLog);
    } catch (Exception e) {
        log.warn("Failed to create audit log entry", e);   // never propagate
    }
}

@Override
public Object postCall(EOperation op, Object param, Object ret) {
    try {
        // secondary logic: statistics, tracking
    } catch (Exception e) {
        log.warn("Interceptor failed", e);
    }
    return ret;   // always return the payload
}

for (Entity item : items) {
    try {
        service.process(item);
        count++;
    } catch (Exception e) {
        log.error("Failed to process item", e);   // continue with the next item
    }
}
```

## Rationale

- Secondary concerns do not take the business operation down, and a partial batch still makes progress.
- Inside a synchronous interceptor the catch is the only thing that keeps a failing side effect from rolling back the user's write.
- The price is silent failure: lost audit rows are not recovered, and a warn log line is easy to miss. Alert on the log message if the data matters.

## Example

In one application the audit service catches everything around its create call, several interceptors catch and log and return the payload unchanged, and the post-expiration job handles each order or request on its own and continues after a failure. In a workflow example the guard evaluation catches the expression engine's missing-property errors and treats them as a false guard, while rethrowing all other expression errors (see [[spel-guard-evaluation]]).

## When to avoid

- The side effect is part of the business rule: a mandatory audit trail that must commit with the change should fail the operation and roll back instead.
- You need retries or recovery: use a queue or a retry job, not a log line.
- Business and validation errors: they must reach the caller through the declared fault or `ValidationException`.

## Related

- [[audit-event-trail]] — the audit writes that are often wrapped this way
- [[quartz-scheduled-job]] — per-item catch inside scheduled jobs
- [[interceptor-aggregation-postcall]] — a postCall that does secondary work
- [[spel-guard-evaluation]] — the narrow catch for a missing context attribute

---
id: "safe-failure-pattern"
title: "Safe Failure Pattern for Non-Critical Operations"
domain: "backend"
category: "error"
score: 57.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
  - workflow-poc
---
## Description

A defensive error handling pattern where non-critical operations (audit logging, analytics, notifications) are wrapped in try-catch blocks that log failures but never propagate exceptions. This ensures that failures in secondary operations do not break the primary business operation. Applied consistently across audit log services, interceptors, and scheduled jobs.

## Structure

```java
// Audit logging - never throws
public void log(ActionType type, String entityType, String entityId, Map details) {
    try {
        // Create audit log entry
        auditLogDao.create(auditLog);
    } catch (Exception e) {
        log.warn("Failed to create audit log entry", e);
        // Never propagate
    }
}

// Interceptor - never breaks operation flow
@Override
public Object postCall(EOperation op, Object param, Object ret) {
    try {
        // Interceptor logic (statistics, tracking)
    } catch (Exception e) {
        log.warn("Interceptor failed", e);
    }
    return ret;  // Always return payload
}

// Scheduler - continue processing remaining items
for (Entity item : items) {
    try {
        service.process(item);
        count++;
    } catch (Exception e) {
        log.error("Failed to process item", e);
        // Continue with next item
    }
}
```

## Examples

### mlszksz-platform
Applied in 3 contexts: (1) `AuditLogServiceImpl.log()` wraps all audit creation in try-catch, never propagates. (2) All 5 interceptors catch exceptions and log warnings, returning payload as-is. (3) `PostExpirationJob` processes each offer/request individually, catching per-item failures and continuing. Ensures business operations succeed even when audit/analytics/cleanup fails.

### workflow-poc
`WorkflowUtils.evalBoolExpression()` catches `SpelEvaluationException` for guard evaluation. When `PROPERTY_OR_FIELD_NOT_READABLE` or `PROPERTY_OR_FIELD_NOT_READABLE_ON_NULL` errors occur (missing context attribute), returns `false` (guard fails safely) rather than propagating the exception. Other SpEL errors are re-thrown. This ensures workflow transitions fail gracefully when context attributes are not yet defined.

## Trade-offs

- Pros: Business operations never fail due to secondary concerns, resilient to partial failures, simple to implement
- Cons: Silent failures can hide bugs, no retry mechanism, lost audit entries not recoverable, warn-level logging may be missed
- Alternative: Dead letter queue for failed operations, async processing with retry, circuit breaker pattern

## Related Patterns

- audit-event-trail
- quartz-scheduled-job
- interceptor-aggregation-postcall

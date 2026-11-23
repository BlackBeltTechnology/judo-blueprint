---
id: state-lifecycle-operation
title: State Lifecycle Management via Bound Operations
description: "Each state transition of an entity is a bound operation that re-fetches the entity, checks the current state, sets the new state, records metadata and persists, with optional side effects such as audit rows."
aliases: [state transition operation, lifecycle operations, status change operation]
keywords: [state, lifecycle, transition, bound operation, guard clause, status enum, audit, custom implementation]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:itracker", "project:alba", "project:mlszksz-platform", "project:viterra_demo", "project:judo-demo-miniworkflow", "project:park-here", "project:indamedia-adtrack", "project:workflow-poc", "project:doors-model", "status:established"]
category: operation
status: established
projects: [trivia, rackinspect, itracker, alba, mlszksz-platform, viterra_demo, judo-demo-miniworkflow, park-here, indamedia-adtrack, workflow-poc, doors-model]
evidence: ["trivia:unrecorded", "rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/services/ai_service/aidefectticket/UpdateAnalysisOutcomeCustomImplementation.java", "itracker:unrecorded", "alba:unrecorded", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/post/impl/PostLifecycleServiceImpl.java", "viterra_demo:unrecorded", "judo-demo-miniworkflow:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "workflow-poc:unrecorded", "doors-model:unrecorded"]
alternatives: [script-driven-operations]
related: [entity-re-fetch-pattern, typed-exception-error-handling, data-snapshot-versioning, audit-event-trail, enum-state-machine, script-driven-operations, spel-guard-evaluation, role-based-invitation-guard]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An entity with a lifecycle (draft, finalized, approved, closed) must change state only along allowed paths. Each transition is its own bound operation. The operation checks the current state, performs the change, records when it happened and optionally triggers side effects. The model holds the status enumeration; the operations hold the rules.

## Practice

### Platform base

- This is the documented state-machine workflow pattern: inject DAOs, guard on the current state, do the business logic, set the new state, call `update`, then create associated rows such as tasks or an immutable audit event ([architectural patterns](../../agent-docs/backend/architectural-patterns.md#3-state-machine-workflows)).
- A transition is a custom operation implemented as an OSGi component ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)), or a JCL script operation (`customImplementation = false`, [[script-driven-operations]]).
- A JCL script operation cannot raise a modeled fault and cannot call an OSGi service. The JCL grammar has no `throw` or fault statement and no service-reference form; its statements are declarations, calls, `return`, `unset`, `delete`, `new`, blocks, `if`, `for` and `while`. Put fault-raising logic and OSGi service calls in a Java custom implementation.
- Interceptors, write guards and range interceptors never fire for custom, mapped or script operations. The state guard and the permission check must be written in each operation, or in a service all transitions call ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Hiding the button does not protect it.
- A refused transition is a business error: throw a fault the operation declares. The generated `<Fault>Exception` is checked, and an undeclared fault breaks the build with a `throws` clause error ([modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)). Names such as `ErrorException` or `BusinessErrorException` exist only when the application models faults of that name.
- An interceptor that guards against edits on a terminal state (built-in update on a finished record) can refuse only through `InterceptorCallBusinessException` ([throwing a business error from an interceptor](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)); it does not protect the transition operations themselves.
- Optimistic locking applies to the update only when the payload carries `__version`, which an entity loaded from the DAO does ([optimistic locking](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)). Concurrent transitions on the same row are therefore detected only when you update the re-fetched entity.

### Practice notes: the five steps

This layer is a convention built on the platform, not a platform feature:

1. **Re-fetch** the bound instance through the DAO for current state ([[entity-re-fetch-pattern]]).
2. **Guard**: check the state precondition, optionally also with a model-level computed boolean such as `isAcceptable`, so the UI can enable the button from the same rule.
3. **Transition**: set the new status.
4. **Record**: set the timestamp, and write a history or audit row with from-state, to-state, time, user and message ([[audit-event-trail]]).
5. **Persist** with `update`, then do side effects such as snapshots ([[data-snapshot-versioning]]) or notifications.

- Keep the status enumeration and the allowed transitions in one place (a service or a table), not copied across operations; the cost of the per-operation style is logic spread over many classes ([[enum-state-machine]] for the model side).
- Hard-delete drafts, soft-delete published records, and keep a last-admin style invariant check in the transition that would break it.
- Terminal states are explicit; transitions out of them are refused.

```java
// Example code: Entity, EntityDao, EntityStatus and the fault are generated types
@Override
public ReturnType apply(Entity _this) throws ErrorException {
    // 1. re-fetch for fresh state
    _this = entityDao.getById(_this.identifier()).get();   // prefer orElseThrow with a chosen outcome

    // 2. validate state precondition
    if (_this.getStatus() == EntityStatus.TERMINAL) {
        throw new ErrorException(Error.builder()
            .withCode(ErrorCode.INVALID_STATE).withMessage("Already closed.").build());
    }

    // 3. transition, 4. record metadata
    _this.setStatus(EntityStatus.NEXT_STATE);
    _this.setTimestampOfTransition(LocalDateTime.now());

    // 5. persist
    entityDao.update(_this);
    return result;
}
```

## Rationale

- The rules for a transition live next to the transition, so a reader sees what is allowed from where.
- The same five steps in every operation make the code predictable and easy to review.
- Cost: state logic spreads over many classes, and shared work (score recalculation) gets duplicated unless it moves into a service.

## Example

- An assessment example: result CREATED, STARTED, FINISHED, FAILED or EXCLUDED. Start checks the group is open and the result not terminal; submit checks STARTED, computes score and duration; exclude recalculates the personal best.
- One application: audit records and orders go DRAFT to DONE; task items change status through a task service; an interceptor blocks edits of a finished audit record.
- Two applications: lifecycles written as scripts (new, review, approved or rejected; created through signed and closed), with side effects before the transition.
- One application: product DRAFT, FINALIZED, APPROVED with rollback by revoking approval; each operation checks state and writes an audit event.
- One application: posts DRAFT, PUBLISHED, EXPIRED or DELETED (hard delete for drafts, soft for published), users with last-admin protection.
- Demo applications: report and document lifecycles; the workflow demo writes a history entry per transition and uses computed booleans as guards.
- One application: booking ACTIVE to EXPIRED or DELETED, by cancel, delete, a scheduled job, or a calendar entry that cascades deletion.
- One application: item ONGOING to FINISHED by a daily job; spendings recalculated on every change.
- A workflow example: a token-based state machine where transitions are event-driven and guarded by expressions ([[spel-guard-evaluation]]).

## When to avoid

- The lifecycle is data, not code (admin-defined states): use an entity-based state machine, see [[spel-guard-evaluation]] for runtime guards.
- A single flag toggle: use a generic toggle operation.
- The transition is plain assignment with no checks: a script operation in the model is enough ([[script-driven-operations]]).

## Related

- [[entity-re-fetch-pattern]] — step 1, loading fresh state
- [[typed-exception-error-handling]] — the declared fault thrown for illegal transitions
- [[audit-event-trail]] — recording who did what and when
- [[data-snapshot-versioning]] — snapshot side effects on approval
- [[enum-state-machine]] — the status enumeration on the model side
- [[script-driven-operations]] — transitions written as model scripts
- [[spel-guard-evaluation]] — runtime guard expressions for data-driven lifecycles
- [[role-based-invitation-guard]] — a permission check inside an operation

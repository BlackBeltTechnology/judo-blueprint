---
id: postcall-persisted-state-validation
title: Post-Call Validation of the Persisted Entity
description: "A post-call interceptor on the create and update operations re-loads the persisted entity and checks fields that are required only under some entitlement, throwing field-located validation results so the transaction rolls back."
aliases: [conditional required fields, validate after write, postCall validation, mandatory when entitled]
keywords: [interceptor, postCall, validation, ValidationException, ValidationResult, location, persisted state, conditional required, partial update, rollback]
tags: ["domain:backend", "layer:backend", "project:park-here", "status:single-project"]
category: interceptor
status: single-project
projects: [park-here]
evidence: ["park-here:application/interceptors/src/main/java/hu/blackbelt/park/here/interceptors/usersettings/UserRefundValidationInterceptor.java"]
alternatives: []
related: [interceptor-template-postcall, interceptor-security-filter-validation, interceptor-crud-lifecycle, entity-re-fetch-pattern]
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

Some fields are required only when another flag is set, for example identity data that becomes mandatory once a user is entitled to a refund. On update the input payload is a partial delta: a key that the client did not send is absent, so a rule written against the input would skip the check. A `postCall` interceptor avoids this by validating the entity as persisted, after the write, where the full merged state is visible.

## Practice

### Platform base

- Built-in create and update operations are interceptable; custom, mapped and script operations are not ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Synchronous interceptors run inside the transaction of the operation. An exception from `preCall` or `postCall` rolls back the DAO write of the operation ([ordering and combining](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)).
- For a field rule on one attribute, throw `ValidationException` (400) with the attribute name as `location` ([throwing a business error](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)). A raw `RuntimeException` becomes a generic 500.

### Practice notes: validate the reloaded entity

This layer is a convention built on the platform, not a platform feature:

- **Intercept create and update together** by resolving both operation FQNs in `getOperations`, so one class holds the rule.
- **Take the identifier from the return payload** (`__identifier`) and return unchanged when it is missing.
- **Reload the entity through its DAO** by that identifier (see [[entity-re-fetch-pattern]]). The reloaded entity reflects the merged state, not the delta.
- **Check the conditional rule on the entity**: when the entitlement flags are true (compare with `Boolean.TRUE.equals`, since a flag can be null), require each dependent field to be present and not blank.
- **Collect all failures, then throw once.** Build one `ValidationResult` per missing field with the field name as `location` and a translated message, and throw a single `ValidationException` holding the list, so the form marks every field at once.
- **Add independent rules in the same pass**, for example a value that must be one of a configured list.
- **Keep the UI in step.** The interceptor is the authoritative gate; any client-side rule only mirrors it.

```java
// Example code: entity, field and message names are illustrative
@Override
public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
    UUID id = (UUID) ((Payload) returnPayload).get("__identifier");
    if (id == null) {
        return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
    }
    Account account = accountDao.getById(id).orElse(null);
    if (account == null) {
        return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
    }
    List<ValidationResult> errors = new ArrayList<>();
    if (Boolean.TRUE.equals(account.getIsPremium())) {
        requireString(account.getTaxId(), "taxId", errors);
        requireString(account.getAddress(), "address", errors);
    }
    if (!errors.isEmpty()) {
        throw new ValidationException(errors);   // each ValidationResult carries code, level and location
    }
    return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
}
```

## Rationale

- Validating persisted state is correct for partial updates, where absent keys read as null and would silently pass an input-based check.
- The post-call throw rolls the write back, so no half-valid row stays in the database.
- Field-located results let the client show the message on the right field.
- Cost: the write has already run when the check fails, and the reload is one more read per call. For a rule that needs only the input, a `preCall` check is cheaper.

## Example

A user-management screen has two refund entitlement flags. When either is true, six identity fields are required on the user. Create and update of the user both go through one `postCall` interceptor that reloads the user and returns one field-located error per missing field. A second rule requires the workplace, when set, to be on a configured accepted list. The same rules are mirrored in the form.

## When to avoid

- The rule depends only on the input of a create: validate in `preCall` and skip the reload.
- The rule is a permission refusal, not a field error: use `InterceptorCallBusinessException` with a stable error code ([[interceptor-security-filter-validation]]).
- The rule can be expressed in the model (required attribute, range): prefer the model, which the UI also reads.
- The operation is custom, mapped or script-driven: interceptors do not fire there; validate in the operation.

## Related

- [[interceptor-template-postcall]] — the other use of `postCall`: shaping the returned payload
- [[interceptor-crud-lifecycle]] — hooks on writes
- [[interceptor-security-filter-validation]] — refuse a call on the request side
- [[entity-re-fetch-pattern]] — loading the persisted entity by identifier

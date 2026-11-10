---
id: toggle-boolean-operation
title: Toggle Boolean Flag Operation Pattern
description: A bound custom operation per boolean flag that re-fetches the entity, flips the flag, updates with a one-field mask and optionally re-validates the parent.
aliases: [toggle flag, flip boolean, activate deactivate operation, toggleActive]
keywords: [toggle, boolean, flag, custom operation, active, primary, mask, update, re-fetch, queryContainer]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "project:ubives", "status:emerging"]
category: operation
status: emerging
projects: [rackinspect, mlszksz-platform, ubives]
evidence: ["rackinspect:unrecorded", "mlszksz-platform:unrecorded", "ubives:unrecorded"]
alternatives: []
related: [entity-re-fetch-pattern, mutable-entity-update-pattern, mask-field-projection, service-delegation-pattern, custom-operation-osgi-component, toggle-active-operation]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Flags such as active, primary or billing change often and independently of the rest of the entity. Instead of sending a full update from the client, the model declares one bound operation per flag, and the backend flips it. Each implementation has the same four steps, so they are quick to write and easy to review.

## Practice

### The four steps

1. Re-fetch the entity from `_this.identifier()` with a mask that holds only the flag ([[entity-re-fetch-pattern]]).
2. Flip the flag.
3. Call `update` with the same mask ([[mask-field-projection]]).
4. Optionally load the parent with `queryContainer` and run its validation operation, when the flag takes part in a parent rule (for example "exactly one primary").

```java
@Component(immediate = true, service = ToggleActive.class)
public class ToggleActiveCustomImplementation implements ToggleActive {
    @Reference EntityDao dao;
    @Reference Validate validate; // optional parent validation

    @Override
    public void accept(Entity _this) {
        Entity entity = dao.getById(_this.identifier(), EntityMask.entityMask().withActive())
            .orElseThrow();
        entity.setActive(!entity.getActive());
        dao.update(entity, EntityMask.entityMask().withActive());
        Parent parent = dao.queryContainer(entity, ParentMask.parentMask()).orElseThrow();
        validate.accept(parent);
    }
}
```

`Entity`, `Parent`, `Validate` and the mask methods stand for generated and example project types. The mask builder method names depend on the model.

### Platform facts that shape it

- The operation is a custom operation: a bound operation implemented as an OSGi component that the generated code calls ([Custom Operations](../../agent-docs/backend/custom-operations.md)). Call-interceptors fire only for built-in operations, so none of them runs around a toggle. Any access check, audit entry or derived write that an interceptor does for `update` must be done by the toggle itself (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Read the flag through the getter the model dictates: a `required` Boolean has a plain getter, a non-required one an `Optional` getter, and a missing value is not the same as `false` ([Absent, Null and Empty Are Different](../../agent-docs/backend/data-access-guide.md#absent-null-and-empty-are-different)). Give the flag a model default, or the first flip has to treat an absent value explicitly.
- Every write bumps `__version`, so the signed identifier a client holds becomes stale after a toggle (see [Optimistic Locking](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)). The client must take the identifier from the response or reload.
- A toggle with an empty mask can update every field. Always pass the one-field mask.

### Project layer

The one-class-per-flag layout, the toggle names (`ToggleActive`, `TogglePrimary`, `ToggleBilling`, `ToggleHeadquarters`) and the parent re-validation are project practice. Where the logic is more than a flip, the operation delegates to a service method ([[service-delegation-pattern]]). The model side of an active toggle is described in [[toggle-active-operation]].

## Rationale

- Uniform and predictable, easy to generate, small code per operation.
- The client sends no payload, so it cannot change other fields by accident.
- Cost: one class per toggle. A single generic toggle service parameterised by entity type and field name is the alternative, but the generated operation interfaces are per type, so each still needs a thin class.

## Example

- RackInspect: 24 toggle implementations across address, bank account, e-mail, phone, unit and user entities (active, primary, billing, delivery, headquarters, postal, standalone-storable). Most re-validate the owning partner after the flip.
- mlszksz-platform: two activate-toggle implementations for city and capability master data. Both delegate to a master-data service method, following [[service-delegation-pattern]]. Platform admins use them to disable entries without deleting them.
- Ubives: six enable/disable operation pairs (registration support, user enabled, access enabled). Each delegates to a service method, repeated across several actor views.

## When to avoid

- The flag is one of many fields the user edits together: use the normal update.
- The change must be an atomic transition between states with rules: use a state operation ([[state-lifecycle-operation]]).
- Many flags share one rule and need no separate operations: a single update with validation is smaller.

## Related

- [[entity-re-fetch-pattern]] — the first step
- [[mutable-entity-update-pattern]] — how the update is issued
- [[mask-field-projection]] — the one-field mask
- [[service-delegation-pattern]] — delegation of the flip to a service
- [[custom-operation-osgi-component]] — the component form of the implementation
- [[toggle-active-operation]] — the model blueprint for the operation
- [[state-lifecycle-operation]] — when more than a flag changes

---
id: multi-actor-role-based-projections
title: Multi-Actor Role-Based Transfer Object Projections
description: "The same entities are exposed through a separate transfer object set per actor, so each role sees only the fields and operations it needs."
aliases: [role-based projections, actor projections]
keywords: [actor, role, transfer object, projection, mapped, derived, access]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:reserve-app, project:viterra_demo, project:doors-model, project:ams-model, project:skillmatrix-model, project:mlszksz-platform, status:established]
category: pattern
status: established
projects: [reserve-app, viterra_demo, doors-model, ams-model, skillmatrix-model, mlszksz-platform]
evidence: ["reserve-app:unrecorded", "viterra_demo:unrecorded", "doors-model:unrecorded", "ams-model:unrecorded", "skillmatrix-model:unrecorded", "mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: [actor-based-transfer-projection]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give each actor type its own view of the same domain entities. An administrator sees the full entity. A restricted actor sees a smaller transfer object with fewer fields, read-only derived fields and only the access it needs.

### Projections are per actor, not per entity

Each actor gets its own transfer objects over the shared entities. The entities stay the single source of truth; the transfer objects decide what is visible and editable for each role.

## Structure

The shared entities live in one package. For each actor there is a set of transfer objects that map the same entity, for example `ReservationForPartner` next to a full admin view. A restricted projection keeps only a few attributes. Its display fields are MAPPED (read-only bindings to related entities) or DERIVED (computed from a getter). Transfer objects that carry no stored value are TRANSIENT. Actor types are tied to their principal transfer object, and their accesses name the transfer objects they expose.

A role can be stored as an enumeration on the user entity (for example PARTNER and ADMIN), or implied by the actor type alone. Names follow `<Entity>For<Role>` or `<Role><Entity>` by convention; the names are a convention, not a platform rule.

## Constraints

- A transfer object maps exactly one entity. Its attributes come from that entity or are TRANSIENT or DERIVED.
- A MAPPED attribute is read-only when its binding source is read-only. Such a field cannot be edited through the projection.
- A DERIVED attribute has a getter expression. The getter is evaluated on the transfer object and must return a value of the declared type.
- An actor's access getter has no `self`. Its filter starts from the entity FQN, not from the transfer object.
- A DERIVED access requires a reference-returning expression. For an unrestricted access, use ALL with no getter.
- An actor type that is not effectively anonymous has a realm (default `DEFAULT`) and claims. An anonymous actor (`anonymous` flag set and no mapped principal) shows neither; a mapped principal makes the actor authenticated, whatever the flag.
- Restricted actors need the referenced transfer objects in their closure too. A nested object that the restricted actor reaches must be exposed to that actor, or the reads fail.

## Variations

- **Role enumeration on the user.** A Role enumeration (PARTNER, ADMIN) is stored on the user entity, and each role maps to its own transfer objects.
- **Actor type per user subtype.** Each user subtype carries an actor type reference, so the actor is fixed by the subtype. See [[actor-based-transfer-projection]] for the role-prefixed naming style.
- **Principal-bound actors.** A self-service actor authenticates as its own transfer object and filters with `getVariable("ACTOR", "email")`, so it sees only its own records.
- **Role flag on the principal.** One actor with a role flag (for example `isAdmin`) on its principal transfer object, instead of one actor per role. An access getter can read it with a typed `getVariable("ACTOR", ...)` call in a single filter, and `hiddenBy` on menu items can use a derived boolean on the principal. This is project practice on top of the platform's access and menu rules; see the advanced modeling patterns in the agent-docs.
- **Named service packages per role.** Projections are grouped into service sub-packages per role instead of per actor package.

## When to use

- Several actor types read the same entities with different visibility.
- A restricted actor must not see internal fields, such as logistics or internal flags.
- A self-service actor must see only its own records.

## When to avoid

- There is only one actor, or all actors see the same fields. One set of transfer objects is simpler.
- The difference is only permission. Use access rules on one projection instead of a copy per role.
- The projections drift apart and nobody maintains them. Each copy is code that has to stay in step with the entity.

## Related

- [[actor-based-transfer-projection]] — the same idea as a best practice, with actor packages
- [[derived-attribute-flattening]] — how the display fields of a restricted projection are computed
- [[audit-log-entity]] — a separate log that is usually exposed to one admin actor only

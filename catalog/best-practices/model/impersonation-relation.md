---
id: impersonation-relation
title: Impersonation Relation for Admin-on-Behalf-of Actions
description: "Store a second optional reference to the user next to the owner relation, so an admin can record content created in another user's name, and expose it only on the admin transfer object."
aliases: [on behalf of, proxy author, acting user]
keywords: [impersonation, on behalf of, admin, author, one-way relation, defaultExpression, transfer object per actor]
tags: ["domain:model", "layer:model", "project:alba", "status:single-project"]
category: relation
status: single-project
projects: [alba]
evidence: ["alba:unrecorded"]
alternatives: []
related: [actor-context-variable-lookup, actor-based-transfer-projection, audit-event-entity]
fragment: impersonation-relation
diagram: { kinds: [entity, transfer], members: types }
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An administrator sometimes creates content in the name of another user. Keep the true owner and the acting administrator apart: the entity has its normal ownership relation and a second, optional relation that records who impersonated.

## Practice

### Two one-way associations to the same target

- `author` (`0..1`, association): the owner. Normally the signed-in user.
- `impersonatingAuthor` (`0..1`, association): set only when an admin acts for someone else.

Both are stored, one-way relations to the same user entity (see [relation kinds](../../agent-docs/model/esm_metamodel/structure.md)). Neither needs a partner relation. The impersonation relation is optional so ordinary content leaves it empty.

### Fill the owner from the signed-in user

A relation of a transfer object or entity can carry a default expression. For a persisted actor (the actor's principal is a mapped transfer object over a stored entity) the expression reads the actor's data with `!getVariable('ACTOR', ...)`; for a token-only actor it would be `USER`. Pick the category deliberately: the wrong one returns empty values without a compile error ([ACTOR vs PRINCIPAL vs USER](../../agent-docs/model/advanced-modeling-patterns.md)). Project practice: the owner defaults to the current user, and the admin overwrites it and fills the impersonation relation explicitly. See [[actor-context-variable-lookup]].

### Expose it only on the admin transfer object

Each actor reaches the entity through its own transfer object ([[actor-based-transfer-projection]]). The admin transfer object maps both relations; the author's transfer object maps only `author`. Because a client can only send members that the transfer object contains, a normal author cannot set the impersonation relation. This is project practice built on the platform's per-actor access: the platform itself does not know the meaning of "impersonating".

## Rationale

- The real owner stays correct for queries such as "my products", while the audit view can still show who uploaded it.
- No actor switch or token exchange is needed: the relation is plain data.
- The model records the fact only. It does not check that the caller is an admin: the admin-only access and the exposure on the admin transfer object are the guard.

## Example

A Product has `author` and `impersonatingAuthor`, both pointing to Person. AdminProduct maps title, author and impersonatingAuthor. AuthorProduct maps title and author. In the source project an admin uploaded products in the name of a teacher. Names are neutral stand-ins.

## When to avoid

- Only one person ever acts on the entity: a single owner relation is enough.
- You need a full audit trail of every change and actor: use [[audit-event-entity]].
- Real impersonation of a session (acting as the user across the whole application) is a login concern, not a data relation.

## Related

- [[actor-context-variable-lookup]] — the owner is set from the actor context
- [[actor-based-transfer-projection]] — impersonation is exposed only on the admin transfer
- [[audit-event-entity]] — full change history instead of one extra relation

## Structure diagram

<!-- mermaid:generated fragment=impersonation-relation cli=1.1.0.20261108_202643_d9769d90_develop -->
```mermaid
classDiagram
  class AdminProduct {
    <<Transfer>>
    +String title
  }
  class AuthorProduct {
    <<Transfer>>
    +String title
  }
  class Person {
    <<Entity>>
    +String name
  }
  class PersonView {
    <<Transfer>>
    +String name
  }
  class Product {
    <<Entity>>
    +String title
  }
  AdminProduct ..> Product : maps
  AdminProduct o-- "0..1" PersonView : author
  AdminProduct o-- "0..1" PersonView : impersonatingAuthor
  AuthorProduct ..> Product : maps
  AuthorProduct o-- "0..1" PersonView : author
  PersonView ..> Person : maps
  Product --> "0..1" Person : author
  Product --> "0..1" Person : impersonatingAuthor
```
<!-- /mermaid:generated -->

---
id: gdpr-placeholder-user-on-delete
title: Placeholder User Replaces a Deleted Person's References
description: A singleton, flagged placeholder user (and tenant) is created on demand so that deleting a person can erase their personal data while records they authored stay valid.
aliases: [dummy user, deleted user placeholder, anonymize on delete, right to erasure]
keywords: [GDPR, erasure, placeholder user, isDummy, getOrCreate, singleton, reassign, author, referential integrity, delete user]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: operation
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/DeleteUserServiceImpl.java"]
alternatives: [soft-delete-archive-pattern, guarded-delete-with-deactivate-fallback]
related: [soft-delete-archive-pattern, guarded-delete-with-deactivate-fallback, business-error-vs-generic-operation-error]
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

A person must be erasable (personal data removed) while content they authored, such as posts or inquiries, must remain and keep a valid author reference. Instead of nulling or archiving, the delete repoints every kept reference to one shared placeholder user, then hard-deletes the real user.

## Practice

### Platform base

- The generated DAO of a mapped type offers typed `filterBy<Attribute>` query filters, `create`, `delete`, `set<Relation>` and per-relation `query...()` accessors ([generated DAO behaviour](../../agent-docs/backend/data-access-guide.md)).
- A refusal the user must see is a modeled fault thrown as a checked exception ([modeled faults](../../agent-docs/backend/error-handling-guide.md)).
- Whether a hard delete is rejected by the platform while required relations still point at the entity is not settled by the agent-docs, *verify*; the practice below repoints first so the question does not arise.

### Practice notes: placeholder and reassign

This layer is a convention built on the platform, not a platform feature. It is not a seed or demo marker.

- Model shape: a Boolean `isDummy` on both the user and the account entity, default false.
- A small service `getOrCreateDummyUser()` looks the placeholder up by `isDummy == true` and creates it on first use, so no seed step or migration is needed. Singleton by lookup: the first call creates, later calls reuse.
- The placeholder is inert: suspended status, lowest read-only role, hidden from listings, notifications and e-mail switched off. It lives in its own placeholder account, itself created on demand, suspended, flagged `isDummy`, with its user count hidden.
- The delete service, in order: guard the caller (only a platform administrator, never oneself, never the placeholder: each a business fault with a machine code); fetch the placeholder; repoint each author or owner relation of the target user (scoped to the user's account, loading identifiers only) with `set<Relation>(entity, placeholder)`; delete records that are purely personal (devices, notifications); remove the identity-server account best-effort; suspend the account when the last active user leaves, except admin and placeholder accounts; finally `delete` the user.
- Every other piece of code that lists or counts users or accounts must exclude the flagged rows (the placeholder carries the flag, so filters use `isDummy`).

```java
// Example code: placeholderUserService and the DAOs are generated types
User placeholder = placeholderUserService.getOrCreateDummyUser();
for (Post post : accountDao.queryPost(org).selectList()) {
    if (isAuthoredBy(post, targetId)) postDao.setAuthor(post, placeholder);   // keep content, drop identity
}
inquiryDao.setUser(inquiry, placeholder);
deviceDao.delete(device);          // purely personal: remove
userDao.delete(targetUser);        // now nothing required points at it
```

## Rationale

- Personal data is truly removed (hard delete) while authored content and its integrity survive, which an archive flag cannot offer.
- The placeholder needs no seeding and survives environment resets.
- Cost: authorship is lost for good (the content shows a neutral "deleted user"), and every user listing must remember to hide the placeholder. The repoint loop touches each relation explicitly, so a new author relation added later must be added to the delete service.

## Example

A delete service repoints authored records (for example posts and requests) to the placeholder from `PlaceholderUserServiceImpl`, deletes devices and notifications, and then deletes the user. The attempt to delete the placeholder itself is refused with a `CANNOT_DELETE_PLACEHOLDER` business fault.

## When to avoid

- The person's data may stay, only access must end: use [[soft-delete-archive-pattern]] or an active flag.
- Authorship must stay attributable (audit): use [[guarded-delete-with-deactivate-fallback]] and refuse the delete.
- Few referencing relations are optional: simply clearing them is simpler.

## Related

- [[soft-delete-archive-pattern]] — keeps the record, the opposite trade-off
- [[guarded-delete-with-deactivate-fallback]] — refuses delete when referenced, instead of repointing
- [[business-error-vs-generic-operation-error]] — why the guards raise modeled business faults

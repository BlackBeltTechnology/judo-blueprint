---
id: platform-configuration-singleton
title: Platform Configuration Singleton Entity
description: A singleton Configuration entity that holds platform-wide settings, seeded once and then updated in place, never created or deleted.
aliases: [singleton configuration, settings entity]
keywords: [platform, configuration, singleton, settings, email templates]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, project:rackinspect, project:park-here, status:emerging]
category: pattern
status: emerging
projects: [mlszksz-platform, rackinspect, park-here]
evidence: ["mlszksz-platform:unrecorded", "rackinspect:unrecorded", "park-here:unrecorded"]
alternatives: []
fragment: platform-configuration-singleton
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep every platform-wide setting in one place: the sender address, the base URL, expiry durations and the text of notification templates. Exactly one Configuration row exists. It is seeded when the application starts and afterwards only changed, so the rest of the model can read settings from a known location.

### Exactly one configuration row

The entity is not createable and not deleteable. The single row is created by an initializer or seed step (see [[initializer-entity-with-init-operation]]). Updates change the existing row.

### Settings are read from the singleton

Other entities and services read settings from the one row. They do not keep copies, so a change to the sender address or an expiry is seen everywhere on the next read.

## Structure

The Configuration entity holds plain attributes: text for the sender address, base URL and platform name, integers for expiry durations, and long text for email templates. Variants add numeric business parameters such as a margin percentage, a closing time, or binary document templates. Some variants add a composition to a per-currency or per-item sub-entity. The entity is exposed to the user through a transfer object or an input transfer object that maps onto it. Required attributes are the ones the platform cannot run without; template attributes are often optional.

## Constraints

- Createable and deleteable are false. The row must exist before the first read, so seeding is required.
- Updateable is true when a generated update is wanted. Variants that change settings only through custom operations set updateable to false as well.
- Required attributes are validated by the platform; a missing required value is a field error (ValidationException, HTTP 400).
- An update that changes only some fields must not overwrite the others. Use an input transfer object with optional fields and apply only the non-null ones.
- Interceptors fire only on built-in operations, never on custom ones. A custom update operation that needs an audit or a guard must call that logic itself.

## Variations

- **Updateable singleton with generated update.** The entity is updateable and the generated update operation is exposed. Simple settings screens use this.
- **Singleton with a custom update operation.** The entity is updateable, but updates go through a custom operation that takes an input transfer object with optional fields. Use this when the input shape differs from the entity or when only some fields may change.
- **Fully non-CRUD singleton.** Createable, updateable and deleteable are all false. Settings are changed only by administrators through custom operations or outside the application.
- **Singleton with business parameters.** The same entity also carries margin, closing-time or document-template fields. Keep these on the singleton only when every consumer needs them.

## When to use

- A setting must be the same for every user and changed rarely.
- Email templates and sender details must be edited without a deployment.
- Other entities need one well-known place for expiries or base URLs.

## When to avoid

- A setting differs per user, per organization or per item. Put it on that owner entity instead.
- The values change often or must be versioned. Use a history entry instead.
- You need several configurations side by side. A singleton holds exactly one row.

## Related

- [[initializer-entity-with-init-operation]] — a static initializer seeds the single row
- [[platform-email-template-service]] — reads the email templates from this entity to build messages
- [[multi-actor-role-based-projections]] — the actor that may read or update settings is a projection decision

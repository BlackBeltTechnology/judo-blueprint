---
id: active-inactive-status-enum
title: Active/Inactive Two-State Status Enumeration
description: "A two-value status enumeration with ACTIVE and INACTIVE, used when an entity is either in use or switched off and no third state is needed."
aliases: [active inactive enum, two state status, on off status]
keywords: [active, inactive, two state, status, enumeration, lifecycle]
tags: [domain:model, layer:model, project:viterra_demo, project:sanctuary-backend, project:kozut-eugyfel-client, status:emerging]
category: pattern
status: emerging
projects: [viterra_demo, sanctuary-backend, kozut-eugyfel-client]
evidence: ["viterra_demo:unrecorded", "sanctuary-backend:unrecorded", "kozut-eugyfel-client:unrecorded"]
alternatives: [active-suspended-deactivated-status-enum, toggle-active-operation]
fragment: active-inactive-status-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Track whether an entity is in use with a status enumeration that has exactly two values. An enumeration can take more values later, which a plain boolean flag cannot, and it reads clearly in queries and in the UI.

### Two values, no middle state

The enumeration has ACTIVE and INACTIVE and nothing between them. An entity is either in use or switched off. If a middle state such as suspended is needed, use the three-value pattern instead.

### The enumeration, not a flag

A status enumeration is preferred over a boolean `active` flag when the status may grow. The cost is one more type in the model. If the status will never grow, a boolean is enough.

## Structure

The enumeration has two members. ACTIVE has ordinal 1 and INACTIVE has ordinal 2. An entity that uses it holds one required attribute of this enumeration type as its status. The enumeration itself has no operations and no relations.

## Constraints

- The enumeration has exactly two members. Adding a member changes the pattern and needs its own entry.
- Each value has a fixed ordinal, unique within the enumeration (0 to 9999 in JSL models). Ordinals must not be reused after a value is removed.
- The status attribute on an entity that uses the enumeration is required, so every entity has a value.
- Operations that switch the status are written on the owning entity, not on the enumeration.

## Variations

- **ACTIVE and INACTIVE.** The classic binary form.
- **Active and archived.** The second value means the entity is kept for reference but no longer used. Use this when data must be preserved.
- **Localised names.** Member names in another language, used where the domain vocabulary requires it. The meaning stays the same: open and closed.
- **Open and closed.** A ticket or case that is either still being handled or resolved. Operations move the status between the two values.

## When to use

- An entity is either in use or switched off, and no third state matters.
- The status is shown in lists and filters, and the enumeration reads better than a flag.
- The status may gain values later.

## When to avoid

- A third state such as suspended or deactivated is needed. Use [[active-suspended-deactivated-status-enum]].
- The status is only a yes or no switch with no other meaning. A boolean is simpler.
- The status changes through many steps with rules between them. Use a full state machine.

## Related

- [[active-suspended-deactivated-status-enum]] — the three-value form when a middle state is needed
- [[toggle-active-operation]] — an operation that flips the status between the two values
- [[open-close-status-toggle]] — the same two-state idea with open and closed wording
- [[accept-reject-operations]] — a decision pair that moves a request between two decided states

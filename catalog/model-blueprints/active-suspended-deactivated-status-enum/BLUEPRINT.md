---
id: active-suspended-deactivated-status-enum
title: Active/Suspended/Deactivated Status Enumeration
description: "A three-value lifecycle status with ACTIVE, SUSPENDED and DEACTIVATED, where suspension can be reversed and deactivation is meant to be final."
aliases: [account lifecycle status, tri-state status, suspend deactivate status]
keywords: [active, suspended, deactivated, lifecycle, status, suspend, deactivate]
tags: [domain:model, layer:model, layer:backend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: [active-inactive-status-enum]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Model an account or organization that an administrator can pause and later reactivate, or close for good, with one status value. Suspension is a reversible hold. Deactivation is the end of use, and it is meant not to be reversed.

### Suspension is reversible

An entity in SUSPENDED can return to ACTIVE. The transition is an operation on the owning entity, and it is refused when the current status is not SUSPENDED.

### Deactivation is the end state

DEACTIVATED is meant as the final value. The model does not enforce that on its own: the operations that set it decide whether a deactivated entity can be reactivated.

## Structure

The enumeration has three members with unique integer ordinals: ACTIVE (0), SUSPENDED (1) and DEACTIVATED (2). An owning entity, such as a user or an organization, holds one required attribute of this enumeration type. The enumeration has no operations. The transitions are operations on the owning entity or on a transfer object that exposes it.

## Constraints

- The enumeration has exactly these three members, in this order. Ordinals are not reused.
- The status attribute on the owning entity is required.
- A transition is allowed only from the state the operation expects. For example, reactivation requires SUSPENDED.
- A guard that blocks the last administrator from being suspended or deactivated belongs to the operation's implementation, not to the enumeration.

## Variations

- **Shared enumeration.** The same member names and ordinals are used for several owners, for example users and organizations, so one set of values covers both.
- **Separate enumerations.** Each owner has its own enumeration with the same members. This avoids coupling the owners but duplicates the values.
- **Two-value form.** When no suspension is needed, use the two-value pattern instead.

## When to use

- Administrators must suspend an account temporarily and restore it later.
- Closing an account must be a separate, final step from suspending it.
- The status is shown in admin tables and filtered on.

## When to avoid

- Only an on or off state is needed. Use [[active-inactive-status-enum]].
- Reversal of deactivation is expected but not supported. Model the rule on the operations, or use a different state set.
- The transitions depend on many rules. Use a full state machine.

## Related

- [[active-inactive-status-enum]]: the two-value form without a suspended state
- [[toggle-active-operation]]: a single flip operation between two values
- [[platform-configuration-singleton]]: another entity with an administrative lifecycle

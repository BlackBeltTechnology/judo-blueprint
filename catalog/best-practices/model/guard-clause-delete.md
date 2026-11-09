---
id: guard-clause-delete
title: Guard Clause for Conditional Delete Operations
description: Delete operations include guard clauses that check preconditions before allowing deletion.
aliases: []
keywords: [guard, clause, conditional, delete, operations]
tags: ["domain:model", "layer:model", "project:skillmatrix-model", "status:single-project"]
category: operation
status: single-project
projects: [skillmatrix-model]
evidence: ["skillmatrix-model:unrecorded"]
alternatives: []
related: [soft-delete-active-flag, mapped-operation-delegation]
fragment: pending
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Delete operations include guard clauses that check preconditions before allowing deletion. If the entity is in an active state or has dependent references, the operation returns early without performing the delete. This prevents accidental deletion of entities that are still in use, enforcing business rules within the operation body rather than at the framework level.

## Structure

- Instance operation named `delete` or `deleteEntity`
- Body begins with a guard clause: `if (condition) { return; }`
- Guard checks typically include:
  - Active state: `if (this.active) { return; }` -- cannot delete active entities
  - Active roles: `if (this.isActiveAdmin or this.isActiveHR or ...) { return; }` -- cannot delete users with active roles
- If guard passes, operation performs cascade cleanup (deleting dependent children) then deletes the entity
- UI may show conditional confirmation dialogs based on related derived attributes (e.g., `hasReferences`)

## Examples

### SkillMatrix
`User.deleteUser`: guards against deleting active users -- returns early if any of `isActiveAdmin`, `isActiveHREmployee`, or `isActiveProfessional` is true. Otherwise cascades: deletes all skills, then deletes the user. `Competence.delete`: guards against deleting active competences -- returns early if `this.active`. Otherwise cascades: deletes all skills and skillTargets, then deletes the competence.

### SkillMatrix-Model
Model source confirms both guard-clause delete operations. `Competence.delete()`: `if (this.active) { return; }` then cascades delete of skills and skillTargets. `User.deleteUser()`: `if (this.isActiveAdmin or this.isActiveHREmployee or this.isActiveProfessional) { return; }` then cascades delete of skills. Both use early return (silent failure) rather than exception throwing.

## Trade-offs

- Pros: Prevents accidental deletion of active/referenced entities, business rules in one place, cascade cleanup is explicit
- Cons: Silent failure (returns without error), no error message to the user about why deletion was blocked
- Prefer when: Deletion has preconditions that must be checked and dependent data must be cleaned up

## Related

- [[soft-delete-active-flag]]
- [[mapped-operation-delegation]]


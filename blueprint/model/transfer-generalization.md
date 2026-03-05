---
id: "transfer-generalization"
title: "Transfer Object Generalization (Inheritance)"
domain: "model"
category: "transfer"
score: 42.7
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - skillmatrix-model
  - kozut-eugyfel-model-test
---
## Description

Transfer objects use generalization (inheritance) to extend a base transfer with additional relations and operations. The base transfer provides common attributes (profile view), while derived transfers add role-specific capabilities. Both the base and derived transfers map to the same underlying entity. This avoids duplicating the base attribute set across multiple purpose-specific transfer objects.

## Structure

- Base transfer object maps to an entity and defines common attributes (e.g., profile fields)
- Derived transfer object extends the base and adds:
  - Additional relations (e.g., `skills`, `trainingPlans`)
  - Additional operations (e.g., `approveAllSkills`, `createTrainingPlan`)
- Both base and derived map to the same entity
- Base is used for read-only/summary views; derived is used for full-featured views
- Multiple derived transfers can extend the same base for different actor contexts

## Examples

### SkillMatrix
`professional::Professional` (base) maps to `User` with profile attributes: `email`, `fullName`, `phone`, `dateOfBirth`, `unit` (flattened string), `manager` (flattened string). Two derived transfers: `MyProfessional` extends Professional and adds `skills [0..*]` (CRUD: create/update/delete) and `skillTargets [0..*]` (read-only). `Subordinate` extends Professional and adds `trainingPlans`, `skills`, `targetSkills`, plus manager operations (`approveAllSkills`, `createTrainingPlan`, `completeAllTargets`).

### SkillMatrix-Model
Model source confirms transfer generalization for User projections. Base `Professional` transfer provides common profile attributes. `MyProfessional` inherits and adds self-service skill management. `Subordinate` inherits and adds manager-focused operations and relations. This DRY approach avoids duplicating 6+ profile attributes across 3 related transfer objects.

### KozutEugyfelModelTest
Each actor package has an `IntezendoBejelentes` transfer that extends the actor's `Bejelentes` transfer. The base `Bejelentes` TO provides common read-only attributes (allapot, bejelentoNeve, helyszin, szoveg, targy) and relations (esemenyek, bejelentesTipus, ugyintezo). `IntezendoBejelentes` inherits all base fields and adds bound operations (lezaras, megjegyzes, tovabbitas) for actionable complaints assigned to the user.

## Trade-offs

- Pros: DRY for common attributes, derived transfers inherit profile fields automatically, clean actor-specific extensions
- Cons: Inheritance coupling (changes to base affect all derived), limited to single inheritance, may be confusing if overused
- Prefer when: Multiple transfer objects share a common base attribute set but differ in available relations and operations

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [transfer-object-multiplicity](transfer-object-multiplicity.md)

---
id: "entity-as-enum-pattern"
title: "Entity Instances as Runtime-Extensible Enum Alternative"
domain: "model"
category: "entity"
score: 24.2
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - skillmatrix-model
---
## Description

Instead of using an enumeration type for a fixed set of classification values, the model uses a regular entity with instances created at runtime (typically via the initializer operation). This pattern provides runtime extensibility -- new classification values can be added without schema changes. Each instance carries a name and optionally a score or ordering attribute.

## Structure

- Entity with `name: String` (required) and optional `score: Integer` or ordering attribute
- Instances created in the static initializer operation (e.g., JUNIOR=1, MEDIOR=2, SENIOR=3, EXPERT=4)
- Referenced via `0..1` or `1..1` relations from other entities (instead of an enum-typed attribute)
- Transfer objects expose the entity through range expressions with sorting: `EntityType!sort(l | l.score ASC)`
- UI presents these as selection pickers, indistinguishable from enum dropdowns
- HR/admin actors may have CRUD access to add/modify levels at runtime

## Examples

### SkillMatrix
`SkillLevel` entity has `name: String` (required) and `score: Integer` (required). Initializer creates 4 instances: JUNIOR (score=1), MEDIOR (score=2), SENIOR (score=3), EXPERT (score=4). Referenced by `Skill.approvedLevel`, `Skill.requestedLevel`, `SkillTarget.skillLevel`. Range expression: `SkillLevel!sort(l | l.score ASC)`. HREmployeeActor has CRUD access (C, U) to manage levels at runtime.

### SkillMatrix-Model
Model source confirms `SkillLevel` entity with `name` and `score` attributes. Used in 4+ range expressions across transfers: `SkillLevel!sort(l | l.score ASC)` for level pickers. Contrasts with `LanguageSkillLevel` which is a true enum (BEGINNER, CONVERSATIONAL, FLUENT, NATIVE) -- demonstrating the project's deliberate choice of entity-as-enum for extensible classifications vs fixed enums for stable ones.

## Trade-offs

- Pros: New values added at runtime without schema migration, values can carry additional data (score, description), supports CRUD management by authorized actors
- Cons: No compile-time safety (unlike enums), requires initializer for seed data, reference by relation instead of literal enum value
- Prefer when: Classification values may need to change or expand after deployment; prefer regular enums when values are truly fixed and known at design time

## Related Patterns

- [category-enum-pattern](category-enum-pattern.md) (alternative: fixed enum for stable classifications)
- [initializer-operation](initializer-operation.md)
- [range-expression-filtering](range-expression-filtering.md)

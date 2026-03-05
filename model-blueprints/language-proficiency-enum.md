---
id: language-proficiency-enum
title: "Language Proficiency Skill Level Enum"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - skillmatrix-model
---

## Description

An enumeration representing language proficiency levels, paired with a LanguageSkill junction entity that associates a User with a Language at a specific proficiency level. The enum members follow a progression from lowest to highest proficiency: BEGINNER, CONVERSATIONAL, FLUENT, NATIVE. The LanguageSkill entity carries the proficiency level (typed to this enum), an optional note for additional context, and a required association to a Language reference data entity. LanguageSkill instances are owned by the User entity via COMPOSITION, meaning they are lifecycle-bound to the user.

This pattern is common in HR/talent management systems, job boards, and employee directories where tracking multilingual capabilities is important. The enum-based approach (rather than a numeric score or separate Level entity) works well because language proficiency levels are standardized and unlikely to change.

## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with members like BEGINNER, CONVERSATIONAL, FLUENT, NATIVE or similar language proficiency levels.

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name } }
    relations { items { name memberType relationKind } }
  }
} } }
```

Look for entities named LanguageSkill with a language relation and a level attribute.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "LanguageSkillLevel"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::LanguageSkillLevel", name: "BEGINNER", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::LanguageSkillLevel", name: "CONVERSATIONAL", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::LanguageSkillLevel", name: "FLUENT", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::LanguageSkillLevel", name: "NATIVE", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "LanguageSkill",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::LanguageSkill", name: "level"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::LanguageSkill", name: "note"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::LanguageSkill", name: "language",
  target: "{{NAMESPACE}}::Language", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### skillmatrix-model
- **LanguageSkillLevel enum**: `SkillMatrix::LanguageSkillLevel`
  - Members: BEGINNER(1), CONVERSATIONAL(2), FLUENT(3), NATIVE(4)
  - Ordinals increase with proficiency level

- **LanguageSkill entity**: `SkillMatrix::LanguageSkill` (non-CRUD)
  - Attributes: level (LanguageSkillLevel, req), note (Text, optional)
  - Relations: language (1..1 OneWay ASSOC Language)
  - Owned by User via `languageSkills` [0..*] COMPOSITION

- **Language entity**: `SkillMatrix::Language` (reference data)
  - Attributes: code (String, req, identifier)
  - No relations, no operations
  - Represents ISO language codes (e.g., "en", "hu", "de")

- **Transfer object projections**:
  - hrEmployee::LanguageSkill -- languageCode (DERIVED from language.code), level (MAPPED), note (MAPPED) + language relation (1..1 AGGREGATION Language)
  - hrEmployee::Language -- code (MAPPED)
  - The HR employee can manage language skills for professionals through the Professional TO's `languages` relation

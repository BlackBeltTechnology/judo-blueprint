---
id: language-proficiency-enum
title: Language Proficiency Level Enum
description: A fixed enumeration of language proficiency levels, used by a LanguageSkill entity that links a user to a language at one level.
aliases: [language skill level, proficiency enum]
keywords: [language, proficiency, skill, level, enumeration, ordinal]
tags: [domain:model, layer:model, project:skillmatrix-model, status:single-project]
category: pattern
status: single-project
projects: [skillmatrix-model]
evidence: ["skillmatrix-model:unrecorded"]
alternatives: [environment-enum]
fragment: language-proficiency-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Record how well a person speaks a language, using a small fixed scale. Standard levels are stable, so an enumeration is simpler than a numeric score or a separate level table. Each skill record ties a user to one language at one level.

### Levels run from lowest to highest

The four levels are ordered: beginner, conversational, fluent and native. Ordinals follow the same order, so the levels can be compared in code, though not with an ordering operator in the model expression language.

### The skill belongs to the user

A language skill is part of its user. It is removed with the user and cannot exist alone.

## Structure

The shape has one enumeration, LanguageSkillLevel, with four members in order: BEGINNER, CONVERSATIONAL, FLUENT and NATIVE. It has a Language entity, a reference record with a required identifier code (for example an ISO language code). The LanguageSkill entity is non-CRUD. It holds a required level of the enumeration, an optional note, and one required association to a Language. A User composes zero or more LanguageSkill entities.

## Constraints

- The level is required and must be one of the four enumeration members.
- Enumeration values travel as integer ordinals on the REST wire, and the generated data access also hands them over as ordinals. Ordinals must be unique within the enumeration (0 to 9999 in JSL models). Do not renumber them after data exists, or stored values change meaning.
- The model expression language (JQL) compares enumeration values only for equality (`==`, `!=`). A minimum-level rule that needs ordering (at least FLUENT) is not expressible there; compare ordinals in Java, or list the accepted members explicitly. That ordering rule is project practice.
- A LanguageSkill is composed by its user, so deleting the user removes its skills.
- A LanguageSkill points to one Language. Each language is a shared reference record, not a per-user copy.
- Adding a level in the middle needs a new ordinal, placed in order. Renumbering existing members is not allowed.

## Variations

- **Four-level scale.** The reference case: beginner to native.
- **Shared language reference.** Languages are reference records, and skills point to them.
- **Per-user language list.** The skill is shown inside the user's profile, without a separate page.

## When to use

- A profile or directory records language ability on a standard scale.
- The levels are fixed and rarely change.
- The levels must be compared or sorted.

## When to avoid

- The scale is open-ended or changes often. A reference table is easier to change.
- Only yes or no is needed. A boolean is enough.
- Language certificates with scores are needed. Store the score, not a level.

## Related

- [[environment-enum]] — another fixed enumeration with stable ordinals
- [[active-inactive-status-enum]] — a two-member status enumeration with the same ordinal rules
- [[error-code-enum]] — a stable enumeration used as reference data

---
id: "language-proficiency-enum"
title: "Language Proficiency Skill Level Enum"
score: 30.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - skillmatrix-model
---
## Description

An enumeration representing language proficiency levels, paired with a LanguageSkill junction entity that associates a User with a Language at a specific proficiency level. The enum members follow a progression from lowest to highest proficiency: BEGINNER, CONVERSATIONAL, FLUENT, NATIVE. The LanguageSkill entity carries the proficiency level (typed to this enum), an optional note for additional context, and a required association to a Language reference data entity. LanguageSkill instances are owned by the User entity via COMPOSITION, meaning they are lifecycle-bound to the user.

This pattern is common in HR/talent management systems, job boards, and employee directories where tracking multilingual capabilities is important. The enum-based approach (rather than a numeric score or separate Level entity) works well because language proficiency levels are standardized and unlikely to change.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

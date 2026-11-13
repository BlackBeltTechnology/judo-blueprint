---
id: competence-skill-matrix-cluster
title: Competence and Skill Matrix Cluster with Levels and Approval
description: An entity cluster for recording what each person can do, at which level, with a self-assessed level, a manager-approved level and training targets.
aliases: [skill matrix, competence matrix, competency model]
keywords: [competence, skill, matrix, levels, approval, training target, junction entity]
tags: ["domain:model", "layer:model", "project:skillmatrix-model", "status:single-project"]
category: pattern
status: single-project
projects: [skillmatrix-model]
evidence: ["skillmatrix-model:unrecorded"]
alternatives: [approval-workflow-pattern]
fragment: competence-skill-matrix-cluster
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep one record per person and competence, holding the level the person claims and the level a manager confirms. Training targets then say which level a person should reach by when. The cluster supports skill gap analysis and training planning.

### A skill links a person to a competence with two levels

Each Skill is a junction between a User and a Competence. It holds a requested level (self-assessed) and an approved level (confirmed by a manager). The two level references are separate, so a change request and its approval are both visible.

### Approval copies the requested level

The approve operation copies the requested level to the approved level. A skill counts as approved when both levels are set and equal. Until then, the manager sees a pending request.

## Structure

The Competence entity has a name (required), a strategic flag (required, default false) and an active flag (required, default true). It is the catalog item that people are assessed on. Skills and skill targets point to it; it keeps no list of them.

The SkillLevel entity is reference data: a name (required) and a numeric score (required). A Skill refers to two SkillLevel entries, requested and approved, each optional. A SkillTarget refers to one SkillLevel (required).

The Skill entity holds no stored data. It is a junction with a required one-way association to Competence (1..1), an optional two-way association to User (0..1, partner User.skills), and two optional associations to SkillLevel. Its approve operation is an instance operation.

The SkillTarget entity is a goal: a completed flag and a deadline date. It refers to a SkillLevel (1..1) and to a Competence (1..1), both one-way associations. It is owned by a User through a composition on the User's training plans.

The User entity is the employee. It holds a full name, a many-association to its skills, and the composition of its skill targets. Its operations are a bulk approval of its skills and the creation of a training plan.

## Constraints

- A Skill refers to exactly one Competence. Many skills can point to one Competence.
- The requested and approved levels are optional and independent. Approval is a separate action, not a side effect of setting the requested level.
- A SkillTarget belongs to exactly one User. Deleting the User deletes its targets, because they are a composition.
- Reference data (SkillLevel and Competence) is not created or changed through the people-facing actors.
- Derived names and scores for display are derived attributes (`memberType = DERIVED` with a getter expression), computed on read and not stored on the Skill. The fragment leaves them out, so add them where the screens need them.
- Skill and SkillTarget point to Competence one-way (required association). Competence does not list its skills. A composition cascades deletion, an association does not, so only the User's targets are removed with the User.

## Variations

- **Enumeration instead of reference entity.** When the scale is fixed and small, use an enumeration for the levels. A reference entity is better when the levels are managed by HR and can change. See [[risk-level-enum]] for the enumeration form.
- **Manager approval from a hierarchy.** Approval can be limited to the manager of the person. Use a derived relation to find subordinates, as in [[approval-workflow-pattern]].
- **Language proficiency as a separate scale.** A language skill with its own enumerated level can sit beside this cluster rather than inside it.

## When to use

- People must record their own level and have it confirmed by someone else.
- Training goals must be tracked per person, with a level and a deadline.
- Skill gap reports need the requested and approved level side by side.

## When to avoid

- There is no approval step. A single level per person is simpler.
- The scale is a free text description, not an ordered level. Use a plain text note instead.
- The need is a history of changes to one skill. Use a history entry instead.

## Related

- [[approval-workflow-pattern]]: the general pattern for a request that someone approves
- [[product-with-approval-workflow]]: an approval workflow on a product, for comparison
- [[risk-level-enum]]: an ordered enumeration, the alternative to a reference entity for levels
- [[derived-attribute-flattening]]: how the display names are computed on read instead of stored

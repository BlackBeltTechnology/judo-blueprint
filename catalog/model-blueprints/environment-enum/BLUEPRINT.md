---
id: environment-enum
title: Environment Enum (DEV/TEST/PROD Deployment Stages)
description: "A fixed enumeration of deployment stages (DEV, TEST, PROD) used as a required attribute on resources that belong to one environment."
aliases: [deployment stage enum, environment stage enum]
keywords: [environment, enum, dev, test, prod, deployment, stages, ordinal]
tags: ["domain:model", "layer:model", "project:InterfaceRegister", "status:single-project"]
category: pattern
status: single-project
projects: [InterfaceRegister]
evidence: ["InterfaceRegister:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Classify a resource by the deployment stage it belongs to, using a closed set of three values: development, test and production. Users pick one value from the list; free text is not allowed.

## Structure

One enumeration with three members, DEV, TEST and PROD, stored with ordinals 1, 2 and 3. Deployment-related entities (for example an application instance) carry a required attribute of this enumeration type. Filtering and grouping by stage use the enumeration value directly.

## Constraints

- The enumeration is closed. Adding a stage is a model change, not a data change.
- Member ordinals are persisted and are the wire value (enumerations travel as integer ordinals). They must be unique and between 0 and 9999. Do not renumber existing members; a new stage gets a new ordinal.
- The name is only a model choice. It has nothing to do with the platform's `ENVIRONMENT` variable category, which reads deployment settings at runtime; this enumeration is stored data on a resource.
- The attribute that uses the enumeration is required when every resource must belong to a stage.

## Variations

- **Add a stage (for example a staging or demo stage).** Add one member with the next free ordinal. Existing rows keep their values.
- **Stage as a reference entity.** When stages need their own attributes (URL, owner, freeze date), model them as an entity with a relation instead. See [[category-enum-pattern]] for the choice.
- **Build type as a second enumeration.** Classify how a resource was built with a separate enumeration. It is independent of the stage.

## When to use

- A resource must be tied to exactly one of a small, stable set of deployment stages.
- Stages are part of the domain vocabulary and change rarely.
- Reports or filters group resources by stage.

## When to avoid

- The set of stages is user-maintained or changes often. Use an entity with a relation.
- Stages need attributes or history. Use an entity.
- The value is a free-form label such as a customer-specific environment name.

## Related

- [[category-enum-pattern]]: choosing between an enumeration and an entity for a fixed set of values
- [[active-inactive-status-enum]]: another small fixed enumeration used as a status

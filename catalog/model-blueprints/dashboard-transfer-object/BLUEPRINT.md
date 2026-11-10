---
id: dashboard-transfer-object
title: Dashboard Transfer Object with Statistics
description: A transfer object that maps an entity to serve as an actor's landing dashboard, with operations that delegate to the entity and an optional transient statistics object.
aliases: [dashboard transfer, landing dashboard, actor dashboard]
keywords: [dashboard, transfer, object, statistics, landing, access point, mapped, transient]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, project:InterfaceRegister, status:emerging]
category: pattern
status: emerging
projects: [mlszksz-platform, InterfaceRegister]
evidence: [mlszksz-platform:unrecorded, InterfaceRegister:unrecorded]
alternatives: [panel-dashboard-transfer]
fragment: dashboard-transfer-object
diagram: { kinds: [entity, transfer], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give an actor a landing view that gathers what the actor works with: mapped attributes, creation operations and, when needed, summary counts. The dashboard is a transfer object, so the entity underneath keeps its own rules.

## Structure

A dashboard transfer object maps one entity, and the actor reaches it through a 0..1 access point. It exposes the mapped attributes of the entity, and its operations either map to the entity's operations or are custom. A statistics object is a second, transfer-only type with transient count attributes. It is not createable, updateable or deleteable, and its values are computed when read. It is not stored.

## Constraints

- The dashboard maps one entity. Do not let it map several entities; use one dashboard per entity instead.
- Mapped operations delegate to the entity. Put business rules on the entity, not in the dashboard.
- Statistics counts are transient. They are filled in on read, so they cannot be filtered or sorted in the database.
- Interceptors do not run on custom dashboard operations. Only built-in operations trigger them.

## Variations

- **Minimal dashboard.** Mapped attributes, a derived greeting and factory operations, with no statistics object. Used when the landing view needs only the actor's own data.
- **Full dashboard with statistics.** Adds a statistics object with counts and an optional nested collection of per-group counts. The counts come from built-in reads that an interceptor fills in.
- **Custom operations.** Dashboard operations implemented in project code, for work that spans several services. Keep them thin.

## When to use

- An actor needs one landing view with several kinds of data at once.
- The landing view shows counts that the actor cannot get from a single list.
- Factory operations for the main entities belong on the actor's home screen.

## When to avoid

- The view only lists one entity. Use the entity's own list.
- The counts must be exact in the database or sorted by the server. Use stored counters instead.
- The dashboard would need several mapped entities. Split it into one dashboard per entity.

## Related

- [[panel-dashboard-transfer]] — the same transfer-object role described as a UI entry point
- [[interceptor-derived-statistics-calculation]] — how the statistics counts are filled in on read
- [[mapped-operation-delegation]] — how transfer operations delegate to the entity
- [[derived-attribute-flattening]] — flattening navigation into attributes on a transfer object

---
id: identifier-adaptation-pattern
title: Identifier Adaptation for Mapped Transfer Objects
description: "Use the SDK identifier adaptTo() to turn the identifier of one mapped transfer object type into the identifier of another type mapped to the same entity, so another DAO can load the entity through a different view."
aliases: [adaptTo, identifier conversion, transfer object view switch]
keywords: [identifier, adaptTo, mapped transfer object, dao, view, type-specific identifier]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:alba", "status:emerging"]
category: data-access
status: emerging
projects: [trivia, alba]
evidence: ["trivia:unrecorded", "alba:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Several transfer objects can be mapped to the same entity, each exposing different fields and relations (a view). An operation bound to one of them sometimes needs to load or return another view. The SDK identifier converts to the identifier type of the other view.

## Practice

### Platform base

Identifiers are type specific: an identifier of one transfer object type cannot be used for another type ([signed identifiers and wire contract](../../agent-docs/backend/platform-behavior-reference.md)). In custom operations the typed identifier is read with `identifier()` ([data access guide](../../agent-docs/backend/data-access-guide.md)). The integration-testing guide marks `adaptTo()` as unnecessary when you only want the identifier of an instance that already has the right type: use `identifier()` there ([anti-pattern: adaptTo to get identifiers](../../agent-docs/integration-testing/best-practices.md)). The agent-docs do not describe `adaptTo()` for converting between different transfer object types. That use is project-observed.

### Practice notes: adapt across views of one entity

Use `adaptTo(<TargetIdentifier>.class)` only when the source and target transfer objects map the same underlying entity and the target DAO is the one that exposes what you need.

```java
// Example code: Order and OrderSummary are two transfer objects mapped to one entity
PromptListIdentifier plId = _this.identifier().adaptTo(PromptListIdentifier.class);
PromptList plist = promptListDao.getById(plId).orElseThrow();
```

- Use it when an operation receives one view but must return or work on another.
- Do not use it for the identifier of an instance that already has the target type: call `identifier()`.
- Check that the result is a different view, not a different entity: adapting between unrelated types is not meaningful.
- Prefer the single `getById` of the target DAO over querying and re-building the view by hand.

## Rationale

- Typed identifiers stay type-safe and no raw ids are handled.
- It relies on the model's mapped transfer object structure and works only for transfer objects mapped to the same entity, so it needs knowledge of that mapping.
- Alternative: query the entity directly and build the needed view manually.

## Example

- A start operation bound to an order view returns a summary view, adapting the identifier and loading it through the other DAO; a submit operation does the same.
- Operations such as finalize, assign approval, approve version, draft new version and revoke approval adapt the bound `_this` identifier to the product identifier type required by the product DAO.

## When to avoid

- The identifier already has the type the DAO needs: use `identifier()`.
- The two transfer objects map different entities: navigate with a relation query instead ([[dao-fluent-query-filter]]).

## Related

- [[dao-fluent-query-filter]] — loading entities with the generated query API
- [[dual-dao-pattern]] — accessing one entity through two DAOs

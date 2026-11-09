---
id: dual-dao-pattern
title: Dual DAO Injection (Entity-Level + Actor-Level)
description: Some custom operations inject both entity-level DAOs (full entity representation with all fields/relations) and actor-level DAOs (restricted view with only actor-visible fields).
aliases: []
keywords: [dual, dao, injection, level, actor]
tags: ["domain:backend", "layer:backend", "project:trivia", "status:single-project"]
category: di
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [custom-operation-osgi-component, identifier-adaptation-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Some custom operations inject both entity-level DAOs (full entity representation with all fields/relations) and actor-level DAOs (restricted view with only actor-visible fields). This provides access to both the complete entity data for backend processing and the actor-specific mapped view for returning constrained results to callers.

## Structure

```java
@Reference
TestDao testDao;  // Entity-level DAO (full access)

@Reference
hu.blackbelt.app.api.app.actors.player.test.TestDao playerTestDao;  // Actor-level DAO (restricted view)
```

Entity-level DAOs reside in `api.[app]._default_transferobjecttypes.entities.[entity]` package.
Actor-level DAOs reside in `api.[app].actors.[actor].[entity]` package.

## Examples

### Trivia
`EnterCustomImplementation` injects both `TestDao` (entity-level, for full CRUD operations) and `hu.blackbelt.trivia.api.trivia.actors.player.test.TestDao` (player-level, for actor-scoped view). The actor-level DAO is injected but not actively used in the current implementation.

## Trade-offs

- Pros: Access to both full entity and actor-constrained views, respects model-level access control
- Cons: Can be confusing with same class name from different packages, unused injection adds noise
- Alternative: Use only entity-level DAO and manually filter/restrict fields before returning

## Related

- [[custom-operation-osgi-component]]
- [[identifier-adaptation-pattern]]


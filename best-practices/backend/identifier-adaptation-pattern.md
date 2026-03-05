---
id: "identifier-adaptation-pattern"
title: "Identifier Adaptation for Mapped Transfer Objects"
domain: "backend"
category: "data-access"
score: 22.7
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - alba
---
## Description

The JUDO SDK `adaptTo()` mechanism converts between identifier types for mapped transfer objects that share the same underlying entity. When multiple transfer object types map to the same entity (e.g., `Test` and `PromptList` both map to the test entity), their identifiers can be adapted to access the same database row through different "views."

## Structure

```java
// Convert Test identifier to PromptList identifier
PromptListIdentifier plId = _this.identifier().adaptTo(PromptListIdentifier.class);

// Use the adapted identifier with a different DAO
PromptList plist = promptListDao.getById(plId).get();
```

This is used when:
- Two transfer objects map to the same underlying entity
- You need to access the entity through a different "view" (different fields/relations exposed)
- The operation receives one TO type but needs to return another

## Examples

### Trivia
`StartCustomImplementation` receives a `Test` but needs to return a `PromptList`. Uses `_this.identifier().adaptTo(PromptListIdentifier.class)` to convert the Test identifier to a PromptList identifier, then loads via `promptListDao.getById()`. Same pattern in SubmitCustomImplementation.

### ALBA
Operations use `_this.identifier().adaptTo(ProductIdentifier.class)` to convert the bound operation's `_this` identifier to the specific `ProductIdentifier` type needed by `productDao.getById()`. Used in Finalize, AssignApproval, ApproveVersion, DraftNewVersion, and RevokeApproval operations.

## Trade-offs

- Pros: Type-safe identifier conversion, avoids raw ID manipulation, leverages JUDO's mapped TO architecture
- Cons: Only works for TOs mapped to the same entity, requires understanding of the model's TO mapping structure
- Alternative: Query the entity directly and manually construct the needed view

## Related Patterns

- dao-fluent-query-filter
- dual-dao-pattern

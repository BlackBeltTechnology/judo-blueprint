---
id: option-order-randomization
title: Option and Item Order Randomization for Anti-Cheating
description: "Applications that grade choice-based items shuffle option positions when items are imported and item order when a set is created, so no two sessions see the same layout."
aliases: [answer-shuffling-anti-cheat, answer shuffling, assessment shuffling, answer randomization, option shuffling]
keywords: [shuffle, randomization, options, anti-cheat, import, set creation]
tags: ["domain:backend", "layer:backend", "project:trivia", "status:single-project"]
category: operation
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

When items are graded by choice, a fixed option position or a fixed item order makes answers easy to share. Two layers of randomization address this: option positions are shuffled when items are imported, and the item sequence is shuffled when a set is created.

## Practice

This is plain Java business logic inside custom operations; the platform contributes only the operation hook ([custom operations](../../agent-docs/backend/custom-operations.md)) and the DAO calls used to persist the result ([data access](../../agent-docs/backend/data-access-guide.md#crud-operations)). The shuffling itself is a practice built on the platform.

### Shuffle option positions at import

Shuffle the list of option slots once per item, remap each choice to its new slot and remap the stored solution accordingly. Keep the mapping between old and new letter in one place so the solution cannot drift from the choices.

```java
// Example code (import operation)
List<String> order = new ArrayList<>(List.of("A", "B", "C", "D"));
Collections.shuffle(order);
builder.withChoiceA(choiceMap.get(order.get(0)))
       .withChoiceB(choiceMap.get(order.get(1)))
       .withSolution(choices.get(String.valueOf((char) ('A' + order.indexOf(originalAnswer)))));
```

### Shuffle item order at set creation

Draw items by shuffled position indices, add the fixed items, then shuffle the combined list again so fixed items do not stay at predictable places.

```java
// Example code (set creation operation)
List<Integer> positions = IntStream.range(0, total).boxed().collect(toList());
Collections.shuffle(positions);
// pick items by the shuffled indices, add fixed ones
Collections.shuffle(selectedItems);
```

## Rationale

- Two independent layers: a leaked answer key by position is useless, and so is a leaked item sequence.
- Cost: `Collections.shuffle()` without a seed is not cryptographically secure and not reproducible in tests; pass a seeded `Random` in tests. Shuffling at import makes the option order permanent for that item.

## Example

An upload operation shuffles the A to D positions while importing items and recomputes the solution letter by index arithmetic. Its enter operation selects items through shuffled indices, includes the fixed items and shuffles the final list again.

## When to avoid

- When the option order carries meaning (for example scales such as "never ... always").
- When each user must see a different order on every display: shuffle at read time instead of at import time.

## Related

- [[bulk-json-import-export]] — import operation where options are shuffled
- [[state-lifecycle-operation]] — session lifecycle around the shuffled attempts

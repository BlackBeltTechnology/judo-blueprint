---
id: answer-shuffling-anti-cheat
title: Answer and Question Shuffling for Anti-Cheating
description: "Quiz applications shuffle answer positions when questions are imported and question order when a test is created, so no two sessions see the same layout."
aliases: [quiz shuffling, answer randomization]
keywords: [shuffle, randomization, quiz, anti-cheat, import, test creation]
tags: ["domain:backend", "layer:backend", "project:trivia", "status:single-project"]
category: operation
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

In a quiz or test application, a fixed answer position or a fixed question order makes answers easy to share. Two layers of randomization address this: answer positions are shuffled when questions are imported, and the question sequence is shuffled when a test is created.

## Practice

This is plain Java business logic inside custom operations; the platform contributes only the operation hook ([custom operations](../../agent-docs/backend/custom-operations.md)) and the DAO calls used to persist the result ([data access](../../agent-docs/backend/data-access-guide.md#crud-operations)). The shuffling itself is project practice.

### Shuffle answer positions at import

Shuffle the list of answer slots once per question, remap each choice to its new slot and remap the stored solution accordingly. Keep the mapping between old and new letter in one place so the solution cannot drift from the choices.

```java
// Example project code (trivia import operation)
List<String> order = new ArrayList<>(List.of("A", "B", "C", "D"));
Collections.shuffle(order);
builder.withChoiceA(choiceMap.get(order.get(0)))
       .withChoiceB(choiceMap.get(order.get(1)))
       .withSolution(choices.get(String.valueOf((char) ('A' + order.indexOf(originalAnswer)))));
```

### Shuffle question order at test creation

Draw questions by shuffled position indices, add the fixed questions, then shuffle the combined list again so fixed questions do not stay at predictable places.

```java
// Example project code (trivia test creation operation)
List<Integer> positions = IntStream.range(0, total).boxed().collect(toList());
Collections.shuffle(positions);
// pick questions by the shuffled indices, add fixed ones
Collections.shuffle(selectedQuestions);
```

## Rationale

- Two independent layers: a leaked answer key by position is useless, and so is a leaked question sequence.
- Cost: `Collections.shuffle()` without a seed is not cryptographically secure and not reproducible in tests; pass a seeded `Random` in tests. Shuffling at import makes the answer order permanent for that question.

## Example

The trivia project's upload operation shuffles the A to D positions while importing questions and recomputes the solution letter by index arithmetic. Its enter operation selects questions through shuffled indices, includes the fixed questions and shuffles the final list again.

## When to avoid

- When the answer order carries meaning (for example scales such as "never ... always").
- When each user must see a different order on every display: shuffle at read time instead of at import time.

## Related

- [[bulk-json-import-export]] — import operation where answers are shuffled
- [[state-lifecycle-operation]] — test lifecycle around the shuffled sessions

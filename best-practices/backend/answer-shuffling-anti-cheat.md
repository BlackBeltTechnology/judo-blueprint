---
id: "answer-shuffling-anti-cheat"
title: "Answer and Question Shuffling for Anti-Cheating"
domain: "backend"
category: "operation"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

Two-layer randomization to prevent cheating in quiz/test applications: (1) answer position shuffling during question import so the correct answer is not always in the same position, and (2) question order shuffling during test creation so each test has a unique question sequence. Both use `Collections.shuffle()` for randomization.

## Structure

Answer shuffling (during import):
```java
List<String> order = new ArrayList<>(List.of("A", "B", "C", "D"));
Collections.shuffle(order);
// Remap choices to new positions
builder.withChoiceA(choiceMap.get(order.get(0)))
       .withChoiceB(choiceMap.get(order.get(1)))
       .withSolution(choices.get(String.valueOf((char)('A' + order.indexOf(originalAnswer)))));
```

Question shuffling (during test creation):
```java
List<Integer> positions = IntStream.range(0, total).boxed().collect(toList());
Collections.shuffle(positions);
// Select questions using shuffled indices
// Then shuffle final list for additional randomness
Collections.shuffle(selectedQuestions);
```

## Examples

### Trivia
Upload operation shuffles answer positions [A,B,C,D] when importing questions, remapping the solution letter using character arithmetic. Enter operation shuffles question selection order using shuffled position indices, includes fixed questions, then shuffles the combined list again for final order.

## Trade-offs

- Pros: Two layers of randomization, simple implementation, effective for casual cheating prevention
- Cons: `Collections.shuffle()` uses unseeded Random (not cryptographically secure), shuffling at import time means shuffled order is permanent
- Alternative: Shuffle at display time (more flexible), use seeded random for reproducibility in testing

## Related Patterns

- bulk-json-import-export
- state-lifecycle-operation

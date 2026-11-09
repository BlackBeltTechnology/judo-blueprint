## Overview

The personal best flag is maintained by custom backend operations that compare a newly submitted test score against the player's existing best for the same contest, updating the `personalBest` boolean flag accordingly. The exclude operation recalculates the personal best when a test is administratively removed.

## Implementation Pattern

- The `SubmitCustomImplementation` class handles personal best calculation during test submission
- After scoring the test (counting correct answers and computing duration), it queries for the player's current personal best using `contestDao.queryTests()` filtered by `filterByPlayerEmail()` and `filterByPersonalBest(BooleanFilter.isTrue())`
- If no previous personal best exists, the current test is marked as personal best
- If a previous best exists, the new test replaces it when: (a) the new score is higher, or (b) the scores are equal but the new duration is shorter (tiebreaker by speed)
- The previous best's `personalBest` flag is set to false before the new one is set to true, maintaining the invariant of exactly one personal best per player per contest
- The `ExcludeCustomImplementation` handles personal best recalculation when a test is excluded: it clears the flag on the excluded test, then iterates all remaining FINISHED tests for that player/contest to find and mark the new best
- Both operations use `testDao.update()` to persist flag changes on both the old and new personal best records

## Examples

### trivia
- Key files: `custom/.../_default_transferobjecttypes/entities/test/SubmitCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/test/ExcludeCustomImplementation.java`
- Pattern: Submit calculates score from correct prompts via `BooleanFilter.isTrue()` count, queries existing personal best with `filterByPersonalBest(BooleanFilter.isTrue())`, compares score (higher wins) then duration (shorter wins as tiebreaker), atomically swaps the flag between old and new best
- Notable: Exclude performs a full recalculation by iterating all FINISHED tests for the player (filtered by `EnumerationFilter.equalTo(TestStatus.FINISHED)`) to find the new best, handling the edge case where the excluded test was the only attempt (no new best set)

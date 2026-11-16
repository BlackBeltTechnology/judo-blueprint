## Backend guidance

The flag is kept by custom operations. Their bodies, and the helper names below, are project code, not platform API. Custom operations are never intercepted, so the rule lives in the operation. See [interceptors](../../agent-docs/backend/interceptors.md).

### Submit sets the flag

After scoring an attempt (for example from the answers given and the elapsed time), the submit operation looks up the participant's current best for the event with the generated DAO query: filter on the participant, filter on `personalBest` with a boolean filter set to true. See [data access guide](../../agent-docs/backend/data-access-guide.md).

- No previous best: the new attempt becomes the best.
- Previous best exists: the new attempt wins when its score is higher, or when the score is equal and the duration is shorter.
- On a win, clear the flag on the old attempt first, then set it on the new one, so exactly one attempt carries it. Persist both with the DAO update.

### Exclude recalculates

When an administrator excludes an attempt, clear its flag, then scan the participant's remaining finished attempts for that event (filter on status with an enumeration filter), pick the best by the same rule and set its flag. If the excluded attempt was the only one, no new best is set.

### Do both writes in one operation

Clear and set the flag in the same operation, so one call leaves one flagged attempt. This is project practice; the platform does not enforce the single-best rule.

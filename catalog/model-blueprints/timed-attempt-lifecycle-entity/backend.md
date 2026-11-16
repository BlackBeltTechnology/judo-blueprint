## Overview

The attempt lifecycle is driven by four custom operations: one creates the attempt when a participant joins, one starts the timer, one submits the answers and computes the result, and one administratively excludes the attempt. Each operation checks the current status before it changes it.

## Implementation pattern

- **Creation.** The enter operation (on the session) creates an attempt in the Created status with a new identifier and the current timestamp. It also creates the items, selected from the session's approved pool.
- **Start.** The start operation allows only the Created status. It sets the start timestamp and returns the items.
- **Submit.** The submit operation allows only the Started status. It matches each answer to an item, records whether it was correct, and computes the score and the duration from the start and finish timestamps. It then sets the Finished or Failed status.
- **Exclude.** The exclude operation can run from any status. It sets the Excluded status. If the attempt held the personal-best flag, it recomputes the flag for the participant's remaining attempts.
- **Status checks.** Each operation reloads the attempt at the start, so it works on current data, and rejects an invalid status with a modeled fault (HTTP 422). The fault must be declared on the operation in the model, or the generated interface has no `throws` clause ([custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations), [modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)).
- **Interceptors.** Interceptors fire only for built-in operations ([interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). These four are custom, so each one must carry its own status check and permission check.
- **Errors.** Business rule violations use the modeled fault type. The example project's own error types are project code, not platform API.

## Examples

### Example

- Example project code: the enter operation on the session, and the start, submit and exclude operations on the attempt.
- Enter selects questions from the approved pool, shuffles them, and creates the items in order.
- Submit uses the timestamps to compute the duration in seconds, and returns the full item list with the solutions shown.
- The personal-best recomputation is in exclude. The ranking pattern covers the rule in more detail.

## Overview

The player screen drives the attempt through its lifecycle. It enters the session, starts the attempt, collects the answers and submits them. It keeps the attempt state in local storage so a reload during the run does not lose the answers.

## Implementation pattern

- **Calls in order.** The start button chains the enter, list and start calls. The submit action sends the answers and shows the result.
- **Persisting the run.** The attempt identifier, the session data, the item list, the answers and the remaining time are kept in local storage. A reload restores the screen from this copy.
- **Initial answers.** When the attempt starts, the screen creates an answer list with a "no answer" value for each item, and fills it in as the participant answers.
- **Errors.** The screen reads the error code from a failed call and shows a message. Some codes trigger a fresh registration, others only show a notice.
- **Results.** After submit, the results are sorted by item number and shown in a results view.
- **Screen state.** A union type tracks the current page (contests, a contest, a prompt, a scoreboard, or none).

## Examples

### trivia

- Framework: React (example project code).
- Key files: `src/App.tsx` (the lifecycle orchestration) and `src/trivia/commons.ts` (shared types).
- The start handler opens the prompt dialog after the three calls succeed. The submit handler opens the results view.
- The per-item timer uses the response time returned after enter.

## Overview

The test/attempt lifecycle entity manifests in the React frontend as a custom state machine managed entirely within the player `App.tsx`, orchestrating the enter-start-submit flow across multiple dialogs with localStorage-based state persistence for crash recovery.

## Implementation Pattern

- **Lifecycle orchestration in App.tsx**: The custom `App.tsx` manages the full test lifecycle through a sequence of service calls: `ActorsplayerContestServiceImpl.enter()` (creates the test), `PlayerServiceForTestsImpl.start()` (transitions to STARTED and returns the prompt list), and `PlayerServiceForTestsImpl.submit()` (sends answers and returns results).
- **State persistence**: The test ID, contest data, prompt list, answer list, and test duration are all persisted to `localStorage` during the flow, enabling the player to recover their session if the browser is refreshed mid-test.
- **Answer list generation**: On test start, the app generates an initial answer list with `Choice.NONE` for each prompt, which is progressively filled as the player answers questions in the `PromptListDialog`.
- **Error handling across lifecycle stages**: The `startClicked` handler chains `enter` and `start` calls, with error handling that parses `ErrorCode` from the response (e.g., `INVALID_CODE` triggers re-registration, `CONTEST_NOT_OPEN` / `TEST_ALREADY_STARTED` show error snacks).
- **Results processing**: After `submit`, the response is sorted by prompt number and displayed in the `ResultsDialog`. The dialog then offers navigation to the `ScoreboardDialog`.
- **Page state management**: A `PageType` union type (`'contests' | 'contest' | 'prompt' | 'scoreboard' | 'none'`) tracks the current view, with transitions driven by user actions and lifecycle events.

## Examples

### trivia
- Framework: React
- Key files: `src/App.tsx`, `src/trivia/commons.ts`
- Pattern: Custom `App.tsx` manages the enter->start->submit lifecycle via three service classes. State is persisted to `localStorage` for crash recovery. The `startClicked` handler chains `enter` + `list` + `start` calls, then opens `PromptListDialog`. On completion, `onSubmit` calls `submit` and displays `ResultsDialog`.
- Notable: The test duration (`responseTime`) is sourced from the test's `responseTime` attribute (fetched after enter) and passed to `PromptListDialog` for per-question timing. The answer list is pre-generated with `Choice.NONE` defaults.

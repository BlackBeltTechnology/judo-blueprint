## Overview

The Test entity lifecycle is managed by four custom operation classes: Enter (creates a test), Start (begins the timer), Submit (scores and finishes the test), and Exclude (administratively removes a test). Each operation enforces status preconditions and throws structured errors for invalid state transitions.

## Implementation Pattern

- `EnterCustomImplementation` (on Contest) creates a new Test when a player joins:
  - Validates contest is OPEN, user credentials are valid (email+code with active flag), then fails any existing STARTED or CREATED tests for the same player
  - Creates a Test entity with CREATED status, UUID id, and current timestamp
  - Selects random questions from the contest's approved question pool, shuffles them, and creates Prompt composition entities numbered sequentially
  - Uses `Collections.shuffle()` for randomization and respects fixed-question lists alongside random selection
- `StartCustomImplementation` transitions CREATED -> STARTED:
  - Validates contest is OPEN and test status is exactly CREATED (rejects STARTED, FINISHED, FAILED, EXCLUDED)
  - Sets `timestampOfStarted` to `LocalDateTime.now()` and returns the prompt list
- `SubmitCustomImplementation` transitions STARTED -> FINISHED:
  - Validates contest is OPEN, test is STARTED (not CREATED, FINISHED, FAILED, or EXCLUDED)
  - Iterates submitted answers, matches each to a Prompt by number, checks correctness against the question's solution, and updates the Prompt
  - Computes score (count of correct prompts), duration (seconds between start and finish timestamps), and personal best flag
  - Returns the full prompt list with solutions revealed
- `ExcludeCustomImplementation` transitions any state -> EXCLUDED:
  - Sets status to EXCLUDED and recalculates the personal best for the affected player if the excluded test held that flag
- All operations inject `TestDao` and throw `ErrorException` with domain-specific `ErrorCode` values (CONTEST_NOT_OPEN, TEST_NOT_STARTED, TEST_ALREADY_STARTED, TEST_CLOSED, INVALID_CODE) for state violations
- Operations use `testDao.getById(_this.identifier())` at the start to reload the entity from the database, ensuring fresh state

## Examples

### trivia
- Key files: `custom/.../_default_transferobjecttypes/entities/contest/EnterCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/test/StartCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/test/SubmitCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/test/ExcludeCustomImplementation.java`
- Pattern: Four OSGi `@Component` classes covering the full Test lifecycle; Enter injects 6 DAOs (ContestDao, UserDao, QuestionDao, PromptDao, TestDao, player TestDao) and creates Test + Prompts; Start/Submit/Exclude inject TestDao + supporting DAOs and enforce status guards via ErrorException
- Notable: Enter selects a random subset of approved questions up to the contest's `numberOfQuestions` limit, respecting fixed questions; Submit uses `ChronoUnit.SECONDS.between()` for precise duration calculation; all operations reload the entity at method entry via `getById()` to avoid stale state; the player TestDao is used for returning the PromptList view via `adaptTo(PromptListIdentifier.class)` identifier adaptation

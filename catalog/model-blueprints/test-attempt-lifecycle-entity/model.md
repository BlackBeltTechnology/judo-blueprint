## Examples

### trivia
- **TestStatus enum**: `trivia::entities::TestStatus` -- CREATED(1), STARTED(2), FINISHED(3), FAILED(4), EXCLUDED(5)
- **Test entity**: `trivia::entities::Test` (non-CRUD)
  - Attributes (9): status (req, default: TestStatus#CREATED), score, duration, timestampOfCreation, timestampOfStarted, timestampOfFinished, personalBest (req, default: false), playerEmail, id (req)
  - Relations: contest (1..1 ASSOC to Contest), player (1..1 ASSOC to User), prompts (0..* COMPOSITION to Prompt)
  - Operations: start (INSTANCE), submit (INSTANCE), exclude (INSTANCE)
  - A test is created when a player enters a contest (Contest.enter operation), starts when the player begins answering, and finishes when they submit answers or the time runs out
- **Admin Test TO** (`trivia::actors::admin::Test`):
  - Attributes: status (req), result, duration, timestampOfCreation, timestampOfStarted, timestampOfFinished, personalBest (req), playerEmail, id (req), contest (denormalized string)
  - Operations: exclude (MAPPED) -- admin can exclude tests (e.g., for cheating)
  - Flattened view: contest name denormalized as a string attribute instead of a relation
- **Player Test TO** (`trivia::actors::player::Test`):
  - Attributes: title, playerEmail, playerName, id, responseTime -- minimal view with contest context
  - Operations: start (MAPPED), submit (MAPPED) -- player can start and submit their test
  - The submit operation takes an AnswerList input containing Answer items (number + choice pairs)
- **Prompt entity** (`trivia::entities::Prompt`): composed items within a test
  - Attributes: number (req), answer (req, default: Choice#NONE), correct (req, default: false)
  - Relations: question (1..1 ASSOC to Question)
  - Each prompt presents a question and records the player's answer choice and whether it was correct
- **Player Prompt TO** (`trivia::actors::player::Prompt`):
  - Attributes: question, category, choiceA, choiceB, choiceC, choiceD, number, answer, solution -- denormalized question content for display

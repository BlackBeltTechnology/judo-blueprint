## Examples

### trivia
- **Choice enum**: `trivia::entities::Choice` -- A(1), B(2), C(3), D(4), NONE(5)
  - NONE serves as the default/unanswered sentinel value for the Prompt entity's answer attribute
- **QuestionStatus enum**: `trivia::entities::QuestionStatus` -- REVIEW(1), APPROVED(2), REJECTED(3)
- **Question entity**: `trivia::entities::Question` (non-CRUD)
  - Attributes (8): question (req), choiceA (req), choiceB (req), choiceC (req), choiceD (req), solution (req, Choice enum), identifier (req, default: getVariable("SEQUENCE", "Question")), status (req, default: QuestionStatus#REVIEW)
  - Relations: category (0..1 ASSOC to Category), upload (0..1 ASSOC to Upload)
  - Operations: approve (INSTANCE), reject (INSTANCE), review (INSTANCE)
- **Admin Question TO** (`trivia::actors::admin::Question`):
  - Attributes: question (req), choiceA-D (req), solution (req), identifier, status, categoryName (denormalized)
  - Relations: category (0..1 AGGREGATION)
  - Operations: upload (STATIC), approve (MAPPED), reject (MAPPED), review (MAPPED), download (STATIC)
  - Admin can bulk-upload questions via JSON and bulk-download, plus moderate individual questions
- **Player Prompt TO** (`trivia::actors::player::Prompt`):
  - Attributes: question, category, choiceA-D, number, answer, solution
  - The solution is only revealed in the PromptList returned after test submission; during the test, only question+choices are shown
- The question identifier uses a database sequence for unique numbering across bulk imports

## Examples

### trivia
- **Upload entity** (`trivia::entities::Upload`): non-CRUD
  - Attributes: json (req), timestampOfUpload (req, default: Timestamp!now()), nrOfUploadedQuestions (req)
  - Relations: questions (0..* ASSOC to Question)
  - Each upload records the raw JSON, when it happened, and how many questions were created
- **Question entity** has a back-reference: upload (0..1 ASSOC to Upload)
  - Allows querying which upload batch a specific question came from
- **Admin JsonData TO** (`trivia::actors::admin::JsonData`): unmapped
  - Attributes: json (req)
  - Used as input parameter for the Question.upload operation
- **Admin Upload TO** (`trivia::actors::admin::Upload`): mapped
  - Attributes: json, timestampOfCreation, nrOfUploadedQuestions -- all optional in the TO view
  - Relations: question (0..* AGGREGATION to Question) -- shows uploaded questions
- **Admin Question TO** (`trivia::actors::admin::Question`):
  - Operations: upload (STATIC) -- takes JsonData input, parses JSON, creates questions
  - Operations: download (STATIC) -- exports questions as JSON
  - The upload operation creates an Upload record, parses the JSON, creates Question entities, sets the upload back-reference on each question, and records the count

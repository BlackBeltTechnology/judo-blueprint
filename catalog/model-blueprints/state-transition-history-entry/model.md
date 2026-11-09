## Examples

### judo-demo-miniworkflow
- **Entity**: `MiniWorkflow::DocumentHistoryEntry` (non-CRUD)
  - Attributes: fromState (optional), toState (req), eventTime (req), message (optional)
  - Relations: user (1..1 ASSOC to User)
  - Composed by Document via `documentHistoryEntries` (0..* COMPOSITION)
- **Transfer Object**: `MiniWorkflow::DocumentHistoryEntryTransfer`
  - Attributes: fromState, toState (req), eventTime (req), message, userRepresentation (denormalized user name)
  - Relations: user (1..1 ASSOC)
- When a Document state transition occurs (requestReview, accept, reject, close), a new DocumentHistoryEntry is created recording fromState (previous state), toState (new state), eventTime (when), message (optional reason), and user (who)
- The message field is populated when a reject operation includes a reason via the Message input TO
- DocumentTransfer exposes `documentHistoryEntries` (0..* AGGREGATION) for viewing the full state transition timeline on the document detail page

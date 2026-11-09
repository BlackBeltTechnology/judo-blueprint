## Examples

### judo-demo-miniworkflow
- **Document entity**: `MiniWorkflow::Document` (non-CRUD)
  - Attributes: referenceNumber (req), currentState, ownerRepresentation, isAcceptable, isClosable, isReviewable, isRejectable
  - Relations: files (0..* COMPOSITION to Files), documentHistoryEntries (0..* COMPOSITION to DocumentHistoryEntry), owner (1..1 ASSOC to User)
  - Operations: requestReview (INSTANCE), accept (INSTANCE), reject (INSTANCE), close (INSTANCE)
- **DocumentState enum**: `MiniWorkflow::DocumentState` -- REVIEW_REQUESTED(1), ACCEPTED(2), REJECTED(3), IN_PROGRESS(4), CLOSED(5)
  - State transitions: IN_PROGRESS -> REVIEW_REQUESTED -> ACCEPTED/REJECTED -> CLOSED
- **DocumentTransfer TO**: `MiniWorkflow::DocumentTransfer`
  - Attributes: referenceNumber (req), currentState, ownerRepresentation, plus guard attributes (isAcceptable, isClosable, isRejectable, isReviewable) and their negations (isNotAcceptable, isNotClosable, isNotRejectable, isNotReviewable)
  - Relations: files (0..* AGGREGATION), documentHistoryEntries (0..* AGGREGATION), owner (1..1 ASSOC)
  - Operations: createDocument (STATIC), accept (MAPPED), close (MAPPED), reject (MAPPED), requestReview (MAPPED)
- **NewDocument TO** (unmapped): referenceNumber -- input for createDocument
- **Message TO** (unmapped): message -- input for reject operation (rejection reason)
- **User entity**: `MiniWorkflow::User` with approver (default: false) boolean, used to control who can accept/reject documents

## Examples

### rackinspect
- **Entity**: `rackinspect::entities::DocumentRegistry` (non-CRUD)
  - Attributes (9): documentType (req), prefix (req), financialPeriodStart (req), financialPeriodEnd (req), transitionPeriodStart (req), transitionPeriodEnd (req), startIndex (req), endIndex (req), currentIndex
- **DocumentType enum**: `rackinspect::entities::DocumentType` -- WORK_REPORT(1), FAULT_REGISTRY(5), OFFER(6), ASSESSMENT_SHEET(7), REVIEW_REPORT(8), JOB_SHEET(9)
- Each document type has its own DocumentRegistry instance with independent prefix and sequence range
- The currentIndex is incremented by backend operations when generating new numbered documents

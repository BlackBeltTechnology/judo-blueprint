## Examples

### rackinspect
- **Enum**: `rackinspect::entities::WorkStatus` -- IN_PROGRESS(1), DONE(2), WONT_FIX(3), NOT_STARTED(4)
- **JobSheet entity**: `rackinspect::entities::JobSheet` -- workStatus (req, default: IN_PROGRESS)
  - Relations: jobSheetItem (0..* COMPOSITION), workReport (0..1 ASSOC), offer (1..1 ASSOC), jobTaskFinishedDocuments (0..1 COMPOSITION)
  - Generalizes from a base document entity
- **WorkReport entity**: `rackinspect::entities::WorkReport` -- workStatus (req, default: IN_PROGRESS), startTime, endTime, numberOfWorkers
  - Relations: jobSheet (1..1 ASSOC), finishedJobSheetItems (0..* ASSOC), signedWorkReportDocument (0..1 COMPOSITION)
  - Generalizes from a base document entity

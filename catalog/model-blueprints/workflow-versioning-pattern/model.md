## Examples

### workflow-poc
- **Workflow entity**: `workflow::entities::Workflow` (non-CRUD)
  - Attributes: name (req), headVersionNumber, publishedVersionNumber
  - Relations: versions (0..* ASSOC to WorkflowVersion), head (0..1 ASSOC), published (0..1 ASSOC)
  - Operations: upload (INSTANCE), publish (INSTANCE), commit (INSTANCE)
- **WorkflowVersion entity**: `workflow::entities::WorkflowVersion` (non-CRUD)
  - Attributes: name, label, versionNumber (req), model, diagram, committed (req, default: false), commitComment, commitTime, uploadTime
  - Relations: states (0..* COMPOSITION to State), events (0..* COMPOSITION to Event), initialState (0..1 ASSOC), workflow (1..1 ASSOC back to Workflow), role (0..1 ASSOC), observers (0..* ASSOC to URL)
  - Operations: commit (INSTANCE)
- **Lifecycle flow**: upload YAML -> creates new head version (committed=false) -> commit (sets committed=true, records commitTime) -> publish (makes the version the active published version)
- **Admin Transfer Objects**: `workflow::transfers::admin::Workflow` (with upload operation and versions relation), `workflow::transfers::admin::WorkflowVersion` (with commit operation, exposes model/diagram/version metadata, adds uncommitted derived boolean)
- **Input TOs**: `workflow::transfers::admin::UploadInput` (yaml field), `workflow::transfers::admin::CommitInput` (comment field)

## Overview

The workflow versioning pattern's backend implementation manages the version lifecycle (upload, commit, publish) through a custom upload operation that handles version number incrementing, uncommitted head cleanup, structural entity creation from YAML definitions, and head pointer management.

## Implementation Pattern

- **Upload operation**: An OSGi `@Component` implementing the `upload` instance operation on the parent Workflow entity. The upload operation orchestrates the full version creation lifecycle:
  1. Parses the uploaded YAML file (via `FileStoreService` and Jackson `YAMLFactory`) into a structured definition
  2. Validates the definition name matches the parent entity name
  3. Checks for an existing uncommitted head version -- if found, deletes it (including all composed structural entities) via a utility method and resets the head pointer to the previous committed version
  4. Creates a new WorkflowVersion with `versionNumber = head.versionNumber + 1` (or 1 if no head exists), linked to the parent Workflow
  5. Sets the new version as the Workflow's head pointer via `workflowDao.setHead()`
  6. Creates all composed structural entities (states, transitions, event types) as children of the new version
  7. Sets metadata on the version (model text, generated diagram, uploadTime)
  8. Returns an admin transfer object projection of the created version
- **Version cleanup utility**: A shared `WorkflowUtils` service provides `deleteWorkflowVersion()` which handles cascading deletion -- first removing incoming transitions from all states (to break circular references), then deleting the version entity (which cascades to composed states, transitions, events)
- **Head pointer management**: After deleting an uncommitted head, the code queries the remaining versions ordered by descending versionNumber and resets the head pointer to the latest remaining version
- **Commit and publish operations**: These simpler operations are typically model-defined (setting `committed=true`, `commitTime=now()`, and moving the published pointer), while upload requires custom Java due to YAML parsing and structural entity creation
- **DI wiring**: The upload operation injects `WorkflowDao`, `WorkflowVersionDao`, and all structural entity DAOs via OSGi `@Reference`, plus `FileStoreService` for file access, `DiagramUtils` for diagram generation, and `WorkflowUtils` for version cleanup

## Examples

### workflow-poc
- Key files: `custom/.../entities/workflow/UploadCustomImplementation.java`, `custom/workflow/utils/WorkflowUtils.java`
- Pattern: The `UploadCustomImplementation` (372 lines) implements the full upload-with-versioning lifecycle. It reads YAML via `FileStoreService`, validates cross-references, manages the uncommitted-head cleanup and version number increment, creates States/Transitions/EventTypes as composed children, generates a Mermaid diagram via `DiagramUtils`, and returns an admin TO projection.
- Notable: Version cleanup in `WorkflowUtils.deleteWorkflowVersion()` must explicitly remove incoming transitions before deleting states to handle bidirectional transition-state references. The head pointer reset queries versions `orderByDescending(WorkflowVersionAttribute.VERSION_NUMBER).selectOne()` to find the latest remaining committed version.
- DI: Injects 8 entity DAOs (`WorkflowDao`, `WorkflowVersionDao`, `RoleDao`, `EventTypeDao`, `StateDao`, `TransitionDao`, `ContextTypeDao`, plus an admin `WorkflowVersionDao`), `FileStoreService`, `DiagramUtils`, and `WorkflowUtils`.

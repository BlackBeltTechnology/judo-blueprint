## REMOVED Requirements

### Requirement: Fragment model per model-shaped entry
**Reason**: Fragment models break on every ESM metamodel change and validate invented models, not real ones.
**Migration**: Diagrams are plain Mermaid text drawn from real project models; no model files are stored.

### Requirement: Strictly valid fragment
**Reason**: No fragments remain.
**Migration**: Model shapes are validated in the consuming project's own model with the CLI.

### Requirement: Diagram equals CLI render
**Reason**: No fragments remain to render.
**Migration**: `spec-check` checks Mermaid syntax; authors keep the diagram consistent with `## Model shape`.

### Requirement: Mandatory after sweep, distillation and on release
**Reason**: The fragment check no longer exists.
**Migration**: `check-all` runs after sweeps, distillation and on release.

## MODIFIED Requirements

### Requirement: Pinned CLI and tools
Authoring tools SHALL use the CLI version pinned in the repository. It SHALL be downloaded at build time and never tracked by git. The repository SHALL contain no stored CLI command lists, GraphQL documents or model files for catalog entries.

#### Scenario: Tracked jar
- **WHEN** any `.jar` other than the Maven wrapper is tracked by git
- **THEN** CI fails

#### Scenario: No stored commands or models
- **WHEN** a change adds a `.model` file or a CLI command list for a catalog entry
- **THEN** the merge criteria reject it

# blueprint-sandbox-validation Specification

## Purpose
Keeps the JUDO CLI pinned and untracked for authoring tools, and keeps CLI command lists and model files out of the repository. Fragment models were removed (2026-11-17-remove-fragment-models): diagrams are plain Mermaid.

## Requirements

### Requirement: Pinned CLI and tools
Authoring tools SHALL use the CLI version pinned in the repository. It SHALL be downloaded at build time and never tracked by git. The repository SHALL contain no stored CLI command lists, GraphQL documents or model files for catalog entries.

#### Scenario: Tracked jar
- **WHEN** any `.jar` other than the Maven wrapper is tracked by git
- **THEN** CI fails

#### Scenario: No stored commands or models
- **WHEN** a change adds a `.model` file or a CLI command list for a catalog entry
- **THEN** the merge criteria reject it

# Spec Delta

## Purpose

Proves that every model-shaped catalog entry is a valid JUDO model fragment for the pinned JUDO CLI, and that its published diagram is exactly what the CLI renders for it. No CLI commands are stored anywhere in the repository.

## ADDED Requirements

### Requirement: Fragment model per model-shaped entry
Every entry declaring `fragment: <id>` SHALL have `fragments/<id>.model` outside the catalog. The fragment is an ESM model that the JUDO CLI wrote with `save`. It contains the Sandbox base plus one package `bp::<id>` with neutral element names. The repository SHALL contain no stored CLI command lists or GraphQL documents for building fragments.

#### Scenario: Fragment missing
- **WHEN** an entry declares `fragment: audit-log-entity` and `fragments/audit-log-entity.model` does not exist
- **THEN** the check fails for that entry

#### Scenario: No stored commands
- **WHEN** CI scans the repository outside skill scripts and tests
- **THEN** it finds no CLI command lists, recipe files or GraphQL documents

### Requirement: Strictly valid fragment
Each fragment SHALL pass the CLI's strict validation (ESM constraints, UI derivation constraints and the transform dry-run).

#### Scenario: Strict validation error
- **WHEN** a fragment fails strict validation
- **THEN** that entry fails with the validator output

### Requirement: Diagram equals CLI render
The check SHALL render the fragment's `bp::<id>` package with the CLI's Mermaid command and the entry's diagram options. The output SHALL be identical to the entry's generated block. Apart from `<<external>>` stubs, the render SHALL contain only elements from `bp::<id>`.

#### Scenario: Stale diagram
- **WHEN** a fragment changes and the entry's generated block is not re-rendered
- **THEN** the check fails and prints the diff

#### Scenario: Leaked element
- **WHEN** the render includes a full Sandbox class from outside `bp::<id>`
- **THEN** the check fails

### Requirement: Pinned CLI and tools
The check SHALL use the CLI version pinned in the repository. It SHALL be downloaded at build time and never tracked by git. Generated blocks SHALL record the CLI version that rendered them.

#### Scenario: Tracked jar
- **WHEN** any `.jar` other than the Maven wrapper is tracked by git
- **THEN** CI fails

### Requirement: Mandatory after sweep, distillation and on release
The check SHALL run on every pull request and release build, and on the full catalog after every sweep or distillation batch merges. No release tag SHALL be created unless every fragment passes.

#### Scenario: Post-sweep run
- **WHEN** a sweep batch adds 12 entries
- **THEN** CI checks all fragments, not only the new 12, and reports passed and failed counts

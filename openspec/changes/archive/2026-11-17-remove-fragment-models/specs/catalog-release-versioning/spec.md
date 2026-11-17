## MODIFIED Requirements

### Requirement: Gated, immutable tags
CI SHALL create the tag `v<version>` and a GitHub release only after every gate passes: docs-lint, `kb eval`, agent-docs parity and the redaction check. CI SHALL never move or overwrite an existing tag.

#### Scenario: Gate failure
- **WHEN** `check-all` fails on a feature build
- **THEN** no tag and no release are created for that build

#### Scenario: Tag exists
- **WHEN** a computed tag already exists
- **THEN** CI fails rather than retagging

### Requirement: Release notes
Each GitHub release SHALL list the catalog entries added, changed and removed since the previous tag on the same branch line, and the gate summary.

#### Scenario: Notes generated
- **WHEN** a release is created
- **THEN** its body contains added/changed/removed entry ids and the `check-all` gate results

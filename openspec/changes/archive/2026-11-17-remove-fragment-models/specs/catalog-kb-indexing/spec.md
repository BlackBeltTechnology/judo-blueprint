## MODIFIED Requirements

### Requirement: Single consumable catalog root
All released knowledge SHALL live under one catalog root containing `best-practices/`, `model-blueprints/` and `agent-docs/`. Non-catalog content SHALL live outside that root and SHALL be excluded from indexing. Non-catalog content means `skills/`, `tests/`, `openspec/` and `.pi/`.

#### Scenario: Consumer indexes only the catalog
- **WHEN** a consumer configures the kb git source with `subdir` set to the catalog root
- **THEN** kb indexes no file from `skills/`, `tests/` or `.pi/`

## REMOVED Requirements

### Requirement: Generated structure diagrams
**Reason**: Diagrams were generated from fragment models, which are removed.
**Migration**: See "Plain Mermaid structure diagrams"; the existing diagram text is kept as a plain Mermaid block.

## ADDED Requirements

### Requirement: Plain Mermaid structure diagrams
Every entry with a model shape SHALL contain a structure diagram as a plain ```mermaid block under `## Structure diagram` (blueprints in `model.md`). The diagram SHALL use neutral names and match the entry's model-shape prose. Entries SHALL NOT carry `fragment:` or `diagram:` frontmatter keys.

#### Scenario: Retired key
- **WHEN** an entry declares `fragment: audit-log-entity`
- **THEN** entry lint fails and names the retired key

#### Scenario: Empty diagram section
- **WHEN** `model.md` has `## Structure diagram` without a mermaid block
- **THEN** entry lint fails

#### Scenario: Invalid Mermaid
- **WHEN** a mermaid block does not start with a known diagram type
- **THEN** spec-check fails

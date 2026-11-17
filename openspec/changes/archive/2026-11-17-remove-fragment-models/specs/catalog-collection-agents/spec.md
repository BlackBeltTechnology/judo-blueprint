## REMOVED Requirements

### Requirement: Fragments built only through the CLI
**Reason**: Fragment models are removed.
**Migration**: Diagrams are drawn from real project models with `judo-model-mermaid/scripts/render --model --scope`.

### Requirement: Output conforms before review
**Reason**: Its scenario required a passing fragment, which no longer exists.
**Migration**: Replaced by "Authored entries conform before review".

## MODIFIED Requirements

### Requirement: One job per skill
Each skill's `SKILL.md` description SHALL name one job and when to use it. Skills compose by calling each other's scripts through documented relative paths, never by copying them.

#### Scenario: Author renders through the Mermaid skill
- **WHEN** `judo-blueprint-author` needs a structure diagram from a real model
- **THEN** it calls the `judo-model-mermaid` render script, and no second render implementation exists in the repository

### Requirement: Diagram a project's own model
`judo-model-mermaid` SHALL render Mermaid for a scope of a real JUDO model, read-only. It is the only rendering mode.

#### Scenario: Consumer diagram
- **WHEN** a rackinspect session asks for a diagram of `rackinspect::entities::Fault` with depth 1
- **THEN** the skill renders it with the CLI and leaves the project model unmodified

## ADDED Requirements

### Requirement: Authored entries conform before review
Every entry a skill writes SHALL pass entry lint, spec-check and redaction before it is offered for review.

#### Scenario: Entry with a retired key
- **WHEN** an authored entry carries `fragment:` or `diagram:` frontmatter
- **THEN** it is not offered for merge

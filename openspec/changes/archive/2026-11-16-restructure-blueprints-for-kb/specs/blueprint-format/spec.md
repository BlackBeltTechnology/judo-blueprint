# Spec Delta

## Purpose

Defines the tool-agnostic shape of every catalog entry (model blueprint and best practice). The knowledge stays valid when JUDO tooling changes, and its structure diagrams always reflect what the CLI really builds.

## ADDED Requirements

### Requirement: Blueprint entry layout
Each model blueprint SHALL be a directory `catalog/model-blueprints/<id>/` with `BLUEPRINT.md` plus the layer files `model.md`, `backend.md` and `frontend.md` that apply. `<id>` SHALL be kebab-case and unique across the catalog.

#### Scenario: Valid blueprint directory
- **WHEN** entry lint scans `catalog/model-blueprints/audit-log-entity/`
- **THEN** it finds `BLUEPRINT.md` and at least one layer file, and reports no layout error

#### Scenario: Duplicate id
- **WHEN** two entries declare the same `id`
- **THEN** entry lint fails and names both paths

### Requirement: Abstract description sections
`BLUEPRINT.md` SHALL contain these sections in order: `Intent`, `Structure`, `Constraints`, `Variations`, `When to use`, `When to avoid`, `Related`. The prose names the fragment's elements, attributes, relation kinds and cardinalities without naming a tool.

#### Scenario: Missing section
- **WHEN** a `BLUEPRINT.md` lacks `When to avoid`
- **THEN** entry lint fails and names the file and the section

### Requirement: Best-practice entry shape
Each best practice SHALL be one file `catalog/best-practices/<domain>/<id>.md` with `domain` set to `model`, `backend` or `frontend`. It SHALL have these sections: `Intent`, `Practice`, `Rationale`, `Example`, `When to avoid`, `Related`.

#### Scenario: Domain mismatch
- **WHEN** a file in `best-practices/backend/` carries the tag `domain:model`
- **THEN** entry lint fails

### Requirement: Only descriptions and Mermaid
Catalog content SHALL consist only of descriptive prose, Mermaid diagrams, and generic code samples in layer guidance (Java, TypeScript, JSX). It SHALL NOT contain GraphQL, JUDO CLI invocations, `java -jar` calls, `judo.sh` commands, or any recipe or command list for building model elements.

#### Scenario: GraphQL rejected
- **WHEN** a catalog file contains a `graphql` fence or a `mutation {` block
- **THEN** entry lint fails

#### Scenario: CLI command rejected
- **WHEN** a catalog file contains `create -t EntityType --ns` or `judo-cli` in prose or a fence
- **THEN** entry lint fails

#### Scenario: JSX allowed
- **WHEN** `frontend.md` contains `sx={{ width: '100%' }}` in a `tsx` fence
- **THEN** entry lint passes that file

### Requirement: Generated structure diagrams
Every entry with a model shape SHALL declare `fragment: <id>` and SHALL contain a structure diagram, rendered by the JUDO CLI from that fragment, inside generated markers that name the fragment and the CLI version. Entries without a model shape SHALL declare `fragment: none: <reason>`. Generated blocks SHALL NOT be edited by hand.

#### Scenario: Missing generated block
- **WHEN** an entry declares `fragment: audit-log-entity` but has no generated block
- **THEN** entry lint fails

#### Scenario: Hand edit detected
- **WHEN** the content between generated markers differs from a fresh render
- **THEN** the Sandbox check fails and names the entry

#### Scenario: Backend-only practice
- **WHEN** a backend best practice declares `fragment: none: backend-only`
- **THEN** entry lint requires no generated block

### Requirement: Hand-written behaviour diagrams
Lifecycle and interaction diagrams (`stateDiagram-v2`, `sequenceDiagram`) MAY be hand-written outside the generated markers, and every `mermaid` block SHALL parse.

#### Scenario: Broken diagram
- **WHEN** a `stateDiagram-v2` block has a syntax error
- **THEN** the gate fails with the file and block index

### Requirement: Evidence frontmatter without score
Entries SHALL carry the following and SHALL NOT carry `score`:
- `projects`;
- `evidence` (`project@sha:path`, `session:<id>`);
- `first_seen`, `last_updated`;
- `alternatives`;
- `status`, derived from the number of distinct projects: `single-project` for 1, `emerging` for 2–3, `established` for 4 or more.

#### Scenario: Status derived
- **WHEN** an entry lists 4 distinct projects
- **THEN** entry lint requires `status: established`

#### Scenario: Score rejected
- **WHEN** frontmatter contains `score:`
- **THEN** entry lint fails

# agent-docs-catalog Specification

## Purpose
agent-docs are owned by this repository: the JUDO project template no longer ships them. They are imported once from the template's last version, made kb-conformant, and verified against the judo-ng platform code. The operator reviews every finding before any doc changes.

## Requirements

### Requirement: One-time import from the last template version
The catalog SHALL contain every non-`domain/` agent-doc of the template at `5bddd8b^`, rendered to static markdown, with catalog-only content preserved. No sync with the template SHALL remain afterwards.

#### Scenario: Import complete
- **WHEN** the import has run
- **THEN** every template `agent-docs/<path>.hbs` outside `domain/` has a `catalog/agent-docs/<path>`, and catalog-only sections from before the import are still present

#### Scenario: No sync tooling left
- **WHEN** CI inspects the repository after P1b
- **THEN** no skill or CI job reads agent-docs from the template

### Requirement: Static, harness-neutral docs
agent-docs SHALL contain:
- no Handlebars outside code fences;
- no `SKILL.md` links, `.claude/` paths, judospec or skill frontmatter;
- no sample project names;
- no `domain/` directory.

#### Scenario: Helper leftover
- **WHEN** a doc contains `{{ lowerCase model.name }}` in prose
- **THEN** entry lint fails

#### Scenario: JSX not flagged
- **WHEN** a doc contains `sx={{ mr: 2 }}` inside a `tsx` fence
- **THEN** entry lint passes

### Requirement: kb-conformant agent-docs
agent-docs SHALL:
- have kb frontmatter: `title`, one-sentence `description`, `aliases`, `keywords`, `tags` (`domain:`, `layer:`, `status:platform`);
- have a companion `<name>.agent.md` when over 300 lines or 15000 bytes;
- keep each section within one kb chunk;
- have a DOX `AGENTS.md` per directory;
- be covered by golden queries.

Format work only adds; it SHALL NOT rewrite existing text or headings.

#### Scenario: Agent-doc frontmatter
- **WHEN** an agent-doc lacks `aliases`, `keywords` or `tags`
- **THEN** `entry-lint` fails and names the key

#### Scenario: Stale companion
- **WHEN** a doc gains a `##` section its companion does not list
- **THEN** `entry-lint` fails and names the section

#### Scenario: Golden query
- **WHEN** `kb eval` runs the agent-docs golden queries
- **THEN** each expected doc is in the top 5

### Requirement: Verified against judo-ng, operator-reviewed
Before Pass A, each agent-docs area SHALL be checked against the judo-ng sources at recorded SHAs. Every finding SHALL cite code evidence. Every finding SHALL be accepted, rejected or edited by the operator, and only accepted findings SHALL change docs.

#### Scenario: Wrong claim found
- **WHEN** a backend doc states a dispatcher behaviour that `judo-runtime-core` does not implement
- **THEN** a finding with verdict `wrong`, `repo@sha:path:line` evidence and a proposed text appears in the review file

#### Scenario: Unreviewed change rejected
- **WHEN** a PR changes an agent-doc without a matching accepted finding
- **THEN** review fails

### Requirement: Not part of any skill
The import and the judo-ng verification SHALL be one-time work, kept in the change folder. Reusable skills SHALL NOT contain agent-docs import, sync or platform-verification steps.

#### Scenario: Skills checked
- **WHEN** the `skills/` and `.pi/skills/` trees are searched for agent-docs import or verification steps
- **THEN** none are found

#### Scenario: Sweep finds a doc problem
- **WHEN** a project sweep notices an agent-docs error
- **THEN** it lists it for review in its PR body and does not edit agent-docs

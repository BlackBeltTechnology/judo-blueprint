# catalog-kb-indexing Specification

## Purpose

Makes the catalog fully conformant with the pi-dashboard kb index format, so `kb_search`, `kb_get` and `kb_neighbors` retrieve the right entry without helper scripts, both in this repo and in consumer projects.

## Requirements

### Requirement: Single consumable catalog root
All released knowledge SHALL live under one catalog root containing `best-practices/`, `model-blueprints/` and `agent-docs/`. Non-catalog content SHALL live outside that root and SHALL be excluded from indexing. Non-catalog content means `fragments/`, `skills/`, `tests/`, `openspec/` and `.pi/`.

#### Scenario: Consumer indexes only the catalog
- **WHEN** a consumer configures the kb git source with `subdir` set to the catalog root
- **THEN** kb indexes no file from `fragments/`, `skills/`, `tests/` or `.pi/`

### Requirement: kb-parseable frontmatter
Every catalog markdown file SHALL start with frontmatter that kb's parser accepts:
- single-line scalars or flow/indented lists only, with no `|` or `>` block scalars;
- `title` and `description` present;
- `keywords` and `aliases` providing search terms;
- `tags` providing facets of the form `domain:<d>`, `layer:<l>`, `project:<p>`, `status:<s>`.

#### Scenario: Block scalar rejected
- **WHEN** a file uses `description: >` followed by indented lines
- **THEN** docs-lint fails, because kb would drop the value

#### Scenario: Searchable by alias
- **WHEN** a blueprint declares `aliases: [event log]` and a user searches `kb_search "event log"`
- **THEN** that blueprint is ranked among the top 3 sources

### Requirement: Chunk-friendly headings
Each catalog file SHALL use descriptive headings that name the entry, not generic labels alone. No section body SHALL exceed kb's maximum chunk size (4000 characters) without a sub-heading.

#### Scenario: Oversized section
- **WHEN** a section body exceeds 4000 characters with no sub-heading
- **THEN** docs-lint fails and names the heading path

### Requirement: Cross-entry links
`Related` and `alternatives` references SHALL be `[[id]]` wikilinks or relative markdown links that resolve to an existing catalog file.

#### Scenario: Dangling link
- **WHEN** a `Related` section links `[[missing-entry]]`
- **THEN** docs-lint fails

#### Scenario: Graph neighbours
- **WHEN** `kb_neighbors` is called on an entry with two alternatives
- **THEN** both alternative entries are returned

### Requirement: DOX AGENTS.md per catalog directory
Every catalog directory SHALL contain an `AGENTS.md` with a `| File | Purpose |` table. The table SHALL have one row per entry or file, and each Purpose SHALL be a one-line summary of the entry.

#### Scenario: Lint clean
- **WHEN** CI runs `kb dox lint`
- **THEN** it reports no missing, stale or empty-purpose rows

### Requirement: Retrieval quality gate
The repository SHALL hold a golden query set mapping realistic questions to expected entries. CI SHALL run `kb eval` against a fresh index and SHALL fail when recall@5 falls below the threshold recorded in the repository.

#### Scenario: Regression blocked
- **WHEN** a change lowers recall@5 below the recorded threshold
- **THEN** the docs-lint job fails and reports the metric

### Requirement: Local index hygiene
The project kb config SHALL index the catalog root plus repository docs, and SHALL exclude non-catalog paths. The kb index database SHALL be gitignored.

#### Scenario: Index DB not committable
- **WHEN** a developer runs `git status` after reindexing
- **THEN** no file under `.pi/dashboard/kb/` appears as untracked or modified

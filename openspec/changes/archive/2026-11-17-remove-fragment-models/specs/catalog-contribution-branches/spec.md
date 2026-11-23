## MODIFIED Requirements

### Requirement: Published merge criteria
`judo-catalog-maintain/references/merge-criteria.md` SHALL list the hard gates (check-all on branch plus develop, catalog-only scope, platform evidence or *verify*, generic wording, real evidence paths, no model files, no loss of other projects' citations) and the principles for new entries, added evidence, differing methods, corrections, conflicting branches and status. Contributors and the maintainer use the same document.

#### Scenario: Out-of-scope change
- **WHEN** a project branch changes `skills/`, `.pi/`, `tests/` or CI
- **THEN** that change is reviewed separately and never merged together with catalog content

#### Scenario: Status grows with usage
- **WHEN** a third project branch adds real evidence to an entry and it is merged
- **THEN** the entry's status becomes `emerging` (2 to 3 projects), and `established` at 4 or more

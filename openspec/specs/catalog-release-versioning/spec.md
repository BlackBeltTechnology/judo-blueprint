# catalog-release-versioning Specification

## Purpose
Gives every catalog build an immutable, JUDO NG-style version and git tag. Any project, on any branch, can then pin the exact catalog it was built against as a kb `git` source.

## Requirements

### Requirement: Base version source
The repository SHALL declare its base version once, as the pom `revision` property in `X.Y.Z-SNAPSHOT` form, following the JUDO packages convention. The release base is that value without `-SNAPSHOT`.

#### Scenario: Base derived
- **WHEN** `revision` is `1.1.0-SNAPSHOT`
- **THEN** the build's base version is `1.1.0`

### Requirement: Branch build versions
For pushes to `develop` and for pull requests from `feature/*` (and the other non-master branches), CI SHALL compute the version `<base>.<yyyyMMdd_HHmmss>_<shortSha>_<branch>`, where `<branch>` has `#`, `/`, `.` and `-` replaced by `_`, and parentheses removed.

#### Scenario: Feature branch version
- **WHEN** CI builds commit `ab12cd3` of `feature/JNG-6380_cli_guidance` at 2026-11-10 10:15:00 UTC with base `1.0.0`
- **THEN** the version is `1.0.0.20261110_101500_ab12cd3_feature_JNG_6380_cli_guidance`

### Requirement: Master release version
A merge to `master` SHALL produce the plain base version and a non-prerelease GitHub release. Builds from every other branch SHALL produce prereleases.

#### Scenario: Master release
- **WHEN** a release PR with base `1.0.0` merges into `master`
- **THEN** CI creates tag `v1.0.0` and a GitHub release that is not marked prerelease

### Requirement: Gated, immutable tags
CI SHALL create the tag `v<version>` and a GitHub release only after every gate passes: docs-lint, `kb eval`, agent-docs parity, the redaction check and Sandbox validation. CI SHALL never move or overwrite an existing tag.

#### Scenario: Gate failure
- **WHEN** Sandbox validation fails on a feature build
- **THEN** no tag and no release are created for that build

#### Scenario: Tag exists
- **WHEN** a computed tag already exists
- **THEN** CI fails rather than retagging

### Requirement: Consumer pinning
A consumer project SHALL be able to pin one release tag for both the catalog and the skills:
- in its kb config, as a `git` source with `pin: v<version>` and `subdir: catalog`;
- as a pi package, with `pi install git:<repo>@v<version>`.

Both SHALL resolve to exactly the tagged tree.

#### Scenario: Pin a feature build
- **WHEN** a rackinspect worktree pins `v1.0.0.20261110_101500_ab12cd3_feature_JNG_6380_cli_guidance` and runs `kb index`
- **THEN** its kb results come from that tagged catalog, and the indexed revision equals `ab12cd3`

#### Scenario: Skills at the same tag
- **WHEN** the consumer installs the pi package at the same tag
- **THEN** the installed skills' scripts match that tag's `skills/` tree

#### Scenario: Upgrade is explicit
- **WHEN** a newer build is tagged
- **THEN** the consumer's index does not change until its `pin` is edited

### Requirement: Release notes
Each GitHub release SHALL list the catalog entries added, changed and removed since the previous tag on the same branch line, and the Sandbox validation summary.

#### Scenario: Notes generated
- **WHEN** a release is created
- **THEN** its body contains added/changed/removed entry ids and the count of passed fragment checks

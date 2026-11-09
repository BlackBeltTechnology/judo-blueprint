# Spec Delta

## Purpose

Turns real JUDO development history (exported pi sessions and CLI audit logs) from any JUDO project into reviewed, evidence-backed catalog knowledge. Personal data never enters the repository.

## ADDED Requirements

### Requirement: External corpus contract
The pipeline SHALL read its corpus from a path outside the repository that is given at run time. The corpus contains:
- pi session JSONL (v3) directories, with their meta files;
- optionally, CLI audit logs (`calls*.jsonl`).

The pipeline SHALL NOT copy corpus files into the repository. Project memory files (`MEMORY.md`) are not mined; a reviewer may read them.

#### Scenario: Corpus stays outside
- **WHEN** a run completes
- **THEN** `git status` shows no session or audit file added under the repository

### Requirement: Recurrence-gated signal extraction
The pipeline SHALL extract `fault`, `user_correction`, `ask_user_decision`, `procedure` and `documentation` signals from sessions. It SHALL promote only patterns that recur in at least N distinct sessions, where N is configurable and defaults to 3. Each promoted pattern carries its provenance and confidence.

#### Scenario: One-off ignored
- **WHEN** a CLI failure and fix appear in a single session only
- **THEN** no candidate is produced for it

### Requirement: Routing to exactly one target
Each promoted candidate SHALL be routed to exactly one target:
- `model-blueprints` / `best-practices`: model or behaviour decisions;
- `cli-upstream`: CLI faults, footguns and procedures, reported for the CLI's own docs and skills, never stored in the catalog;
- `agent-docs`: doc gaps and corrections;
- `excluded`: personal preferences or process rules.

#### Scenario: CLI footgun routed out of catalog
- **WHEN** a candidate describes a mutation that fails without a prior `discard --derived`
- **THEN** it is routed to `cli-upstream` and never written into a catalog entry

#### Scenario: Preference excluded
- **WHEN** a candidate states "never commit unless told"
- **THEN** it is routed to `excluded`

### Requirement: Abstracted authoring with evidence
Candidates routed to the catalog SHALL be written in the blueprint-format rules. They SHALL carry `evidence` references (`session:<id>`, `cli-audit:<date>`) and the recurrence count, and SHALL NOT contain transcript text.

#### Scenario: No verbatim transcript
- **WHEN** a distilled entry is generated
- **THEN** no line longer than 40 characters matches the source session text verbatim, outside code identifiers

### Requirement: Redaction gate
Generated content SHALL be rejected if it contains any of the following:
- OS user names or local home paths;
- e-mail addresses, client or customer names, or customer document names;
- tokens or secrets;
- hostnames of private infrastructure.

Rejection names the file and the matched rule.

#### Scenario: Local path leak
- **WHEN** an entry contains `/Users/gaborflorian/projects/rackinspect`
- **THEN** the redaction gate fails

### Requirement: Human review before merge
Distilled candidates SHALL be delivered as a reviewable batch (a pull request or review list) and SHALL NOT be committed to a release branch without explicit human approval.

#### Scenario: No auto-merge
- **WHEN** a distillation run finishes
- **THEN** its output is an unmerged batch awaiting review

### Requirement: Incremental re-runs
The pipeline SHALL keep a watermark per corpus. On a re-run it processes only sessions newer than the watermark, and does not duplicate candidates that were already accepted or rejected.

#### Scenario: New export
- **WHEN** a newer session export is added and the pipeline re-runs
- **THEN** only the new sessions are mined, and previously decided candidates are not proposed again

### Requirement: Contributor consent
The pipeline SHALL refuse to run on a corpus whose contributors are not listed as consenting in a repository-tracked consent record.

#### Scenario: Unlisted contributor
- **WHEN** the corpus contains sessions from a user not in the consent record
- **THEN** the run stops before extraction and names that user

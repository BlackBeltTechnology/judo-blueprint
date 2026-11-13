---
id: workflow-versioning-pattern
title: Workflow/Definition Versioning with Head and Published Pointers
description: "A parent definition entity with an ordered series of version entities and two pointers, head (latest, possibly uncommitted) and published (live), driven by upload, commit and publish operations."
aliases: [head and published version, definition versioning, draft and live version]
keywords: [versioning, head, published, commit, upload, definition, draft, version number]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:workflow-poc", "status:single-project"]
category: pattern
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: [plan-versioning-snapshot]
fragment: workflow-versioning-pattern
diagram: { kinds: [entity, operation], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let a definition (workflow, template, configuration) be edited and tested without touching the version that production uses. New content is uploaded as a head version; only after it is committed and published does it become the live version.

### Draft and live side by side

The head is the newest version and may still be uncommitted. The published version is the one the runtime reads. They may point to the same version or to different ones.

## Structure

A Definition entity has a required name and denormalised headVersionNumber and publishedVersionNumber (integers) for display. It points to its DefinitionVersion entities with three relations: versions (0..*), head (0..1) and published (0..1), all association kind. A DefinitionVersion has a required versionNumber, a required committed flag (default false), commitComment, commitTime, uploadTime, the definition content (text) and an optional diagram (text). It owns the structural elements of the definition (here Step, composition 0..*) so every version is a self-contained snapshot. Definition has two instance operations, upload and publish; DefinitionVersion has commit. All three are custom operations.

## Constraints

### A version is complete and then frozen

A version owns its structural elements, so copying or deleting a version moves or removes the whole snapshot. Once committed it must not change; commit and publish are the only writers of those flags.

### Upload replaces an uncommitted head

Upload deletes an existing uncommitted head, with the structure it owns, and resets head to the latest remaining version before creating version number head+1 (or 1). Committed versions are never deleted. If structural elements point at each other across the version, break those links before deleting.

### Operations are custom, so interceptors do not guard them

Upload, commit and publish are custom operations, which interceptors never see (see [backend.md](backend.md)). State checks, such as "only a committed version can be published", belong in the operation.

## Variations

- Keep the denormalised version numbers as derived attributes (computed from head and published) so they cannot drift.
- Snapshot the data at commit time instead of owning structure per version; see [[plan-versioning-snapshot]].
- Drop the committed flag when every upload is immediately publishable.

## When to use

- Definitions are edited by users and must be testable before they go live.
- The history of definitions must be kept, and the running system must pin to a published version.

## When to avoid

- Changes may go live immediately and history is unimportant: a plain updatable entity is enough.
- Only the data needs history, not a definition: use an audit log or [[data-snapshot-versioning]].

## Related

- [[workflow-engine-state-machine-cluster]] — the workflow engine that uses this pattern for its definitions
- [[plan-versioning-snapshot]] — versions as data snapshots
- [[data-snapshot-versioning]] — snapshot practice for versions
- [[custom-operation-osgi-component]] — how upload, commit and publish are registered

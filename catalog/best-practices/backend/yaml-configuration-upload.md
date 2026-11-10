---
id: yaml-configuration-upload
title: YAML-as-Configuration Upload and Parse Pattern
description: Domain configuration such as a workflow definition is uploaded as a YAML file through the FileStore, parsed in a custom operation with Jackson into typed records, checked for cross-references, and only then turned into entities.
aliases: [yaml upload, configuration as yaml, declarative configuration import, workflow definition upload]
keywords: [yaml, configuration, upload, parse, Jackson, YAMLFactory, FileStore, records, validation, cross-reference, workflow, custom operation]
tags: ["domain:backend", "layer:backend", "project:workflow-poc", "status:single-project"]
category: operation
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: []
related: [filestore-mediated-file-transfer, typed-exception-error-handling, data-snapshot-versioning, builder-pattern-entity-creation, relation-based-entity-creation, staged-import-pipeline]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Domain experts define configuration (workflow definitions, rule sets) as text, without code changes. A custom operation receives the uploaded YAML file, parses it into typed Java records, checks that every reference inside the document resolves, and creates the entity graph from it. Nothing is written until the whole document is valid.

This is project code. The platform provides the upload mechanism and the DAOs; the YAML schema, parser and validation are written by the project.

## Practice

### Receive the file

The operation input has a binary attribute. Upload is two-phase: the client asks for an upload token, uploads the content to the file store with it, and sends the token as the attribute value ([Binary Upload Tokens](../../agent-docs/backend/platform-behavior-reference.md#binary-upload-tokens)). The operation then reads the stored file through the FileStore service ([[filestore-mediated-file-transfer]]). The agent-docs do not document the FileStore service API, so check its signatures in your SDK version.

### Parse into records

Define the schema as Java records with Jackson annotations: `@JsonProperty(required = true)` for mandatory keys, and `@JsonFormat(with = ACCEPT_SINGLE_VALUE_AS_ARRAY)` where a key may be a single value or a list. Read with an `ObjectMapper` built on `YAMLFactory`.

```java
public record YamlData(
    @JsonProperty(required = true) WorkflowData workflow,
    @JsonProperty List<StateData> states,
    @JsonProperty List<TransitionData> transitions) {
    public record WorkflowData(@JsonProperty(required = true) String name) {}
    public record StateData(@JsonProperty(required = true) String name) {}
    public record TransitionData(
        @JsonProperty(required = true) String from,
        @JsonProperty(required = true)
        @JsonFormat(with = JsonFormat.Feature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
        List<String> to) {}
}

String text = new String(fileStore.get(input.getYaml()).readAllBytes());
YamlData data = new ObjectMapper(new YAMLFactory()).readValue(text, YamlData.class);
```

`fileStore` is the project's injected service; the exact call is an example.

### Validate before writing

Check every cross-reference first: the workflow name matches its target, every state, role and event named in a transition exists in the document, and the roles named in the document exist in the database. Collect the problems by category and report them. Parse errors from Jackson are checked exceptions: catch them and convert them, otherwise the client sees a generic 500 ([How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)). Report document problems as a modeled fault declared on the operation, with a code per problem category ([[typed-exception-error-handling]]). The fault must be declared on the operation or the generated interface has no `throws` clause ([Modeled Faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)).

### Materialise

Create the entities in dependency order and keep a name-to-entity map to resolve references: first the version, then events, states, transitions. Contained rows are created through the parent DAO ([[relation-based-entity-creation]], [[builder-pattern-entity-creation]]). Store the original YAML text on the version for traceability ([[data-snapshot-versioning]]).

### Atomicity

A custom operation runs in one transaction, and a thrown exception rolls it back. So validate first and throw before creating, or let a failure during creation roll everything back; do not catch and continue with a half-built graph. Custom operations are not intercepted, so any checks that interceptors do for built-in creates must be done here ([Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

## Rationale

- Declarative configuration without code changes, kept in version control, with rich validation before entity creation.
- Costs: the schema changes mean record changes, parse errors are runtime failures, the cross-reference validation is hand-written, and no IDE help for the custom schema.
- Alternatives: JSON configuration (wider tooling), a UI form, or model-level scripting for tighter platform integration. For tabular bulk data see [[staged-import-pipeline]].

## Example

- workflow-poc: an upload operation parses YAML workflow definitions with record types for workflow, roles, events, states and transitions. It checks that the workflow name matches the target entity, that all state, role and event references exist, and that all roles exist in the database. It creates the workflow version, event types, states and transitions, generates a Mermaid diagram, stores the original YAML on the version, and replaces uncommitted head versions on re-upload.

## When to avoid

- The configuration is small and changes rarely: model enumerations or seed data are simpler.
- Non-technical users must edit it: a UI form gives better feedback.
- The document is large and needs partial acceptance: use a staged import ([[staged-import-pipeline]]).

## Related

- [[filestore-mediated-file-transfer]] — reading the uploaded file
- [[typed-exception-error-handling]] — reporting document problems
- [[data-snapshot-versioning]] — keeping the source with the version
- [[builder-pattern-entity-creation]] — building the entities
- [[relation-based-entity-creation]] — creating contained rows through the parent
- [[staged-import-pipeline]] — import with per-row review

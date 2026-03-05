---
id: "yaml-configuration-upload"
title: "YAML-as-Configuration Upload and Parse Pattern"
domain: "backend"
category: "operation"
score: 18.8
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - workflow-poc
---
## Description

A pattern where domain configuration (e.g., workflow definitions, rule sets) is uploaded as YAML files via the FileStore service, parsed at runtime using Jackson with YAMLFactory, validated against cross-reference rules, and materialized into persistent entity structures. This allows domain experts to define configurations declaratively without code changes, while the backend enforces validation and creates the corresponding entity graph. The YAML schema is defined as Java records with Jackson annotations.

## Structure

```java
// Define YAML schema as Java records
public record YamlData(
    @JsonProperty(required = true) WorkflowData workflow,
    @JsonProperty List<StateData> states,
    @JsonProperty List<TransitionData> transitions
) {
    public record WorkflowData(@JsonProperty(required = true) String name) {}
    public record StateData(@JsonProperty(required = true) String name) {}
    public record TransitionData(
        @JsonProperty(required = true) String from,
        @JsonProperty(required = true)
        @JsonFormat(with = JsonFormat.Feature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
        List<String> to
    ) {}
}

// Parse uploaded YAML
String model = new String(fsService.get(input.getYaml().getId()).readAllBytes());
ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
YamlData yamlData = mapper.readValue(model, YamlData.class);

// Validate cross-references
checkStateExist(yamlData, yamlData.workflow.initial);

// Create entities from parsed data
Map<String, State> stateMap = new HashMap<>();
for (StateData stateData : yamlData.states) {
    State state = versionDao.createStates(version, StateForCreate.builder()
        .withName(stateData.name).build());
    stateMap.put(stateData.name, state);
}
```

Key elements:
- Jackson `ObjectMapper` with `YAMLFactory` for YAML deserialization
- Java records for schema definition with `@JsonProperty` and `@JsonFormat` annotations
- Cross-reference validation before entity creation (all referenced names must exist)
- Declarative error reporting via typed exceptions on validation failure
- Entity maps for resolving name-based references to persisted entities

## Examples

### workflow-poc
`UploadCustomImplementation` parses YAML workflow definitions with 5 record types (`YamlData`, `WorkflowData`, `RoleData`, `EventData`, `StateData`, `TransitionData`). Validates: workflow name matches target entity, all state/role/event references in transitions exist in YAML, all YAML roles exist in database. Creates `WorkflowVersion`, `EventType`, `State`, and `Transition` entities from parsed data. Generates a Mermaid diagram and stores the original YAML text on the version. Replaces uncommitted head versions on re-upload.

## Trade-offs

- Pros: Declarative configuration without code changes, runtime-parseable, version-controlled YAML files, rich validation before entity creation
- Cons: YAML parsing errors are runtime failures, schema evolution requires Java record changes, no IDE support for custom YAML schema, cross-reference validation is manual
- Alternative: JSON configuration (more widely supported), database-driven UI forms (more user-friendly), model-level scripting (tighter platform integration)

## Related Patterns

- filestore-mediated-file-transfer
- typed-exception-error-handling
- data-snapshot-versioning
- builder-pattern-entity-creation

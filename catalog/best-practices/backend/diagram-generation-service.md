---
id: "diagram-generation-service"
title: "Automatic Diagram Generation from Entity Data"
domain: "backend"
category: "service"
score: 43.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - workflow-poc
---
## Description

A utility service pattern that generates visual diagram representations (e.g., Mermaid state diagrams) from persistent entity data. The service is registered as an OSGi component and injected into operations that create or modify the source data. Diagrams are generated using Handlebars templates and stored as text on the parent entity, enabling immediate visualization in the UI without external tooling. The service handles special diagram elements like fork/join stereotypes, initial/final state markers, and annotated transitions.

## Structure

```java
@Component(immediate = true, service = DiagramUtils.class)
public class DiagramUtils {
    @Reference StateDao stateDao;
    @Reference TransitionDao transitionDao;
    @Reference WorkflowVersionDao workflowVersionDao;

    public String getDiagram(WorkflowVersion version) {
        String mermaidTemplate = """
            stateDiagram
            {{#each states}}
            state {{#if name}}"{{name}}" as {{/if}} {{id}} {{{stereotype}}}
            {{/each}}
            {{#each transitions}}
            {{from}} --> {{to}} {{#if event}} : {{event}}{{/if}}
            {{/each}}
            """;

        // Build context maps from entities
        List<Map<String, String>> states = new ArrayList<>();
        List<Map<String, String>> transitions = new ArrayList<>();

        for (State state : workflowVersionDao.queryStates(version).selectList()) {
            // Map state to diagram element (handle join/fork/final stereotypes)
            // Map transitions with event and role annotations
        }

        Handlebars handlebars = new Handlebars();
        Template template = handlebars.compileInline(mermaidTemplate);
        return template.apply(context);
    }
}
```

Key elements:
- OSGi component registered as self-service (`service = DiagramUtils.class`)
- Handlebars inline template for Mermaid syntax generation
- Entity traversal via DAO relation queries (states, transitions, next states)
- Special handling for fork (`<<fork>>`), join (`<<join>>`), and final states (`[*]`)
- Transition annotations with event names and role names
- Diagram stored as string field on parent entity for UI rendering

## Examples

### workflow-poc
`DiagramUtils.getDiagram()` generates Mermaid stateDiagram syntax from a `WorkflowVersion`. Iterates all states, creating Mermaid state declarations with optional stereotypes (join states get `<<join>>` with a secondary labeled state, fork states are auto-generated for multi-target transitions with `<<fork>>`). Final states get an arrow to `[*]`. Transitions are annotated with event IDs and role names. The initial state gets an arrow from `[*]`. The generated diagram is stored on `WorkflowVersion.diagram` after each upload.

## Trade-offs

- Pros: Immediate visual documentation, no external tooling required, Mermaid renders in many UIs, auto-updated on every definition change
- Cons: Limited to Mermaid syntax capabilities, complex diagrams may be hard to read, no layout control (Mermaid auto-layouts), string-based generation is fragile
- Alternative: External diagram generation service, client-side rendering only (no server storage), PlantUML (more feature-rich), custom SVG generation

## Related Patterns

- handlebars-email-template
- token-based-workflow-execution
- data-snapshot-versioning

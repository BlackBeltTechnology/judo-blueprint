---
id: diagram-generation-service
title: Automatic Diagram Generation from Entity Data
description: A service renders a Mermaid diagram from persisted entity data and stores it as text on the parent entity, so the UI can show it without extra tooling.
aliases: [mermaid from data, generated state diagram, diagram utils]
keywords: [diagram, mermaid, handlebars, template, service, state diagram, osgi component, text field]
tags: ["domain:backend", "layer:backend", "project:workflow-poc", "status:single-project"]
category: service
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: []
related: [handlebars-email-template, token-based-workflow-execution, data-snapshot-versioning]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Some entities describe a graph (a workflow of states and transitions). Users understand it faster as a picture. Render a Mermaid diagram text from the stored data whenever that data changes, keep it in a text attribute of the parent entity, and let the frontend render it.

## Practice

### A service builds the text

The renderer is application code (in one application a class called `DiagramUtils`), not a platform feature. It is an OSGi component that custom operations inject with `@Reference`, like any other service (see [Custom Service Layer](../../agent-docs/backend/architectural-patterns.md#2-the-custom-service-layer)).

- Read the source entities through the generated DAO relation queries (`queryStates(version).selectList()`). Use a mask limited to the attributes the diagram shows.
- Turn them into plain maps or lists and feed a template engine (Handlebars in the example) with an inline Mermaid template. Keeping the template as text makes the output easy to test without the platform.
- Single-valued relations return the entity directly, multi-valued ones return a query customizer. Relation queries cannot be ordered, so sort the results in Java if the diagram needs a stable order (see [Relationship Navigation Queries](../../agent-docs/backend/data-access-guide.md#relationship-navigation-queries)).

### Store the result on the parent

The operation that creates or changes the source data calls the service and writes the string to a text attribute of the parent (`diagram` in the example) with a normal DAO `update` and a mask for that one field. Do it in the same operation, so data and picture are saved or rolled back together.

### Handle special nodes explicitly

Fork and join stereotypes, start and end markers and annotated transitions need their own branches in the mapping code. Escape names that contain characters Mermaid treats as syntax by quoting them with an alias.

## Rationale

- The diagram is always consistent with the data, because it is regenerated in the operation that changed the data.
- Storing text avoids rendering on every read and needs no external service.
- Limit: Mermaid decides the layout. Large graphs get hard to read, and string-based generation breaks on unescaped names, so cover the mapping with tests.

## Example

A workflow upload creates a version with states, transitions, events and role assignments. The service walks the states of the version, declares each one (join and fork get stereotypes, final states get an arrow to the end marker), adds one arrow per transition labelled with the event and role, and the result is stored in the version's `diagram` attribute. The frontend renders that text as a state diagram.

## When to avoid

- The graph is large or needs layout control: render client-side with a dedicated library or use a richer diagram tool.
- The diagram is only needed occasionally: compute it on demand instead of storing it.
- The source data is edited through many paths: one regeneration point is hard to guarantee, so do not store a copy that can go stale.

## Related

- [[handlebars-email-template]] — the same template technique applied to e-mail bodies
- [[token-based-workflow-execution]] — the workflow data this diagram visualises
- [[data-snapshot-versioning]] — versions of the data the diagram belongs to

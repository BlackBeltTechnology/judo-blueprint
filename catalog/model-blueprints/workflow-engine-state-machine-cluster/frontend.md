## Overview

The Workflow Engine State Machine cluster manifests in the React frontend through two custom visual element components (Mermaid diagram viewer for state machine visualization, CodeViewer for YAML workflow definitions), an OperationFlowManager for post-operation navigation, and a generator override for redirect-annotated operation outputs. These custom components replace the default text widgets for the WorkflowVersion `diagram` and `model` fields with rich interactive renderers.

## Implementation Pattern

- **Mermaid diagram component**: A custom visual element registered via `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with `componentImplementation: 'Mermaid'`. Uses the `mermaid` library to render state machine diagrams from the WorkflowVersion `diagram` field (which contains Mermaid syntax). The component includes `svg-pan-zoom` for interactive navigation of large diagrams. Bound to data via `boundAttributeName` (the attribute holding the Mermaid source text).
- **CodeViewer component**: A custom visual element registered with `componentImplementation: 'Code'`. Uses `react-syntax-highlighter` (Prism with oneLight theme) to render the WorkflowVersion `model` field as syntax-highlighted YAML with line numbers. Both components are registered as Pandino services in `application-customizer.tsx`.
- **OperationFlowManager**: Handles redirect results from workflow operations (especially `navigate` on tokens and `startWorkflow`). Extracts `idName`/`idValue` for entity navigation or `operation` for page reload after state transitions.
- **Generator override**: The `operation-primary-output-handler.fragment.hbs` template override adds `processRedirect(result)` calls when operation output TOs have a `redirect` annotation, enabling automatic navigation after workflow operations.
- **NPM dependencies**: `mermaid` (diagram rendering), `svg-pan-zoom` (diagram interactivity), `react-syntax-highlighter` (YAML code display).

## Examples

### workflow-poc
- Framework: React
- Key files: `custom/components/Mermaid.tsx`, `custom/components/CodeViewer.tsx`, `custom/components/registerMermaidComponent.tsx`, `custom/components/registerCodeViewerComponent.tsx`, `custom/application-customizer.tsx`, `generator-overrides/ui-react/actor/src/fragments/operations/operation-primary-output-handler.fragment.hbs`
- Pattern: Two `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` Pandino services replace default text rendering for WorkflowVersion fields. The Mermaid component renders the `diagram` attribute as an interactive state machine graph with pan/zoom. The CodeViewer renders the `model` attribute as syntax-highlighted YAML. Both use `GenericProxyProps` with `boundAttributeName` to access the data field.
- Notable: The Mermaid component renders into a 60vh container with `svg-pan-zoom` controls for navigating large state machine diagrams. The CodeViewer uses a 500px max-height scrollable container. Both show a `CircularProgress` spinner while data is loading.

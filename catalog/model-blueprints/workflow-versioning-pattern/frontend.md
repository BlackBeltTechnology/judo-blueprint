## Overview

The Workflow Versioning pattern manifests in the React frontend through custom visual element components that render the version entity's `model` (YAML definition) and `diagram` (state machine visualization) fields as rich interactive widgets instead of plain text areas.

## Implementation Pattern

- **CodeViewer for model field**: A custom visual element registered with `componentImplementation: 'Code'` renders the WorkflowVersion `model` attribute as syntax-highlighted YAML using `react-syntax-highlighter`. This provides a read-only code view with line numbers for inspecting uploaded workflow definitions.
- **Mermaid for diagram field**: A custom visual element registered with `componentImplementation: 'Mermaid'` renders the WorkflowVersion `diagram` attribute as an interactive state machine graph using the `mermaid` library. This provides visual inspection of the versioned workflow structure with pan and zoom.
- **Pandino service registration**: Both components are registered via `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` in `application-customizer.tsx`, making them available to the generated WorkflowVersion detail page wherever the model layout specifies `Code` or `Mermaid` as the custom visual element type.
- **Version lifecycle operations**: The generated frontend handles the upload/commit/publish lifecycle through standard generated action buttons on the admin Workflow and WorkflowVersion pages. No custom hooks are needed for these operations.

## Examples

### workflow-poc
- Framework: React
- Key files: `custom/components/CodeViewer.tsx`, `custom/components/Mermaid.tsx`, `custom/components/registerCodeViewerComponent.tsx`, `custom/components/registerMermaidComponent.tsx`
- Pattern: The CodeViewer renders the `model` YAML with Prism syntax highlighting (oneLight theme, line numbers, max-height 500px scrollable). The Mermaid component renders the `diagram` as an SVG with pan/zoom controls. Both are bound to WorkflowVersion attributes via `boundAttributeName`.
- Notable: The two custom visual elements work together on the WorkflowVersion detail page -- CodeViewer shows the textual definition while Mermaid shows the visual diagram, giving administrators both code-level and graphical views of each version.

---
id: custom-visual-element-override
title: Custom Visual Element Override via Pandino
description: Render a model-designated custom implementation element with your own React component, registered as a Pandino service under the custom visual element key.
aliases: [custom implementation component, component replacement, visual element override]
keywords: [custom implementation, visual element, pandino, component, scaffold, proxy props, ESM UI model]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "project:workflow-poc", "project:park-here", "status:emerging"]
category: component
status: emerging
projects: [rackinspect, workflow-poc, park-here]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/custom-implementations/registerServicesPartner_servicePartnerPartner_View_EditCustomImplementations.tsx", "workflow-poc:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, application-customizer-hub]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Part of a page needs UI the generator cannot produce (charts, masked inputs, rich viewers). Model that part as a custom implementation element and supply the React component yourself; the rest of the page stays generated.

## Practice

### Platform base

- A custom implementation is a visual element of the ESM UI model that the generator exposes as an extension point. It is not a way to swap an arbitrary generated component: the element must be modeled first ([widgets: placeholder / custom implementation](../../agent-docs/frontend/esm-to-ui-mappings/widgets.md), [advanced patterns: custom component replacement](../../agent-docs/frontend/advanced-patterns.md)).
- You register a function component as a Pandino service under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` (exported from `~/custom`) with the service property `component` set to the per-element key generated in the container's `customization.ts`. There is no generic `CUSTOM_COMPONENT_HOOK_INTERFACE_KEY`.
- For containers that have such elements the generator creates the scaffold `src/custom/hooks/custom-implementations/register<Container>CustomImplementations.tsx.default` with one `register<Interface>CustomImplementation(context)` function per element and the right props type (`GenericProxyProps`, `TableProxyProps`, `LinkProxyProps` from `~/custom`). Copy it without `.default`, implement the component and call the register function from `application-customizer.tsx` ([hooks: using .default scaffolds](../../agent-docs/frontend/hooks/README.md)).
- The same service key also carries other custom elements, such as table sidekicks and the AppBar extra component ([table hooks](../../agent-docs/frontend/hooks/table-hooks.md), [UI hooks](../../agent-docs/frontend/hooks/ui-hooks.md)).

```typescript
// from the scaffold (names generated per element)
export function registerMyElementCustomImplementation(context: BundleContext) {
  context.registerService<FC<GenericProxyProps>>(CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY, MyElement, {
    component: MY_ELEMENT_COMPONENT_INTERFACE_KEY,
  });
}
```

### Practice notes

- Keep the component in `src/custom/` and use the props of the proxy type; the data, edit mode and loading state come from it, not from your own fetching.
- Handle every state the generated element would have handled (loading, read-only, validation errors); nothing is inherited.
- Use it only when action hooks, table hooks or theming cannot reach the goal, because each override is code you maintain across model changes.

## Rationale

The element is replaced at one well-defined seam while navigation, data binding and the rest of the page stay generated. The cost is full responsibility for the element's behavior and coupling to the model element and its generated key.

## Example

- A large frontend with many custom implementations, including a configurable form, a masked identifier input, a password-style input and file upload buttons.
- A workflow frontend: two custom elements bound to a transfer object attribute: a diagram renderer for workflow states and a read-only YAML code viewer.

## When to avoid

- A hook, table sidekick or theme change achieves the goal: see [[pandino-action-hook-override]].
- The behavior can be modeled with standard widgets; model it instead of coding it.

## Related

- [[pandino-action-hook-override]] — customizing behavior of generated pages through hooks
- [[application-customizer-hub]] — where the register functions are called

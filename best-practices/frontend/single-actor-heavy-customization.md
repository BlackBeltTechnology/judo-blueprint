---
id: "single-actor-heavy-customization"
title: "Single-Actor Frontend with Heavy Hook Customization"
domain: "frontend"
category: "framework"
score: 6.8
usage_count: 1
alternative_count: 2
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
alternatives:
  - dual-actor-frontend-architecture
  - zero-customization-generated-frontend
---
## Description

A JUDO project with a single actor frontend that relies entirely on the generated page structure but heavily customizes behavior through Pandino hooks, custom visual element overrides, and action hooks. Unlike the dual-actor pattern (one custom + one generated), this approach keeps all pages generated and adds customizations via the hook system. The application-customizer.tsx serves as the central registration hub for 80+ hooks.

## Structure

```
application/frontend-react/
  model__actor/                     # Single actor frontend
    .generator-ignore               # Protects i18n, layout, application-customizer
    src/
      custom/
        application-customizer.tsx  # 100+ Pandino registrations
        hooks/
          custom-implementations/   # Custom visual element components
          dialogs/                  # 48+ dialog action hooks
          pages/                    # 10+ page action hooks
          FormActionsHooks/         # Blur action hooks
          ViewEditActionHooks/      # View/edit hooks
          TableRowHighlightingHooks/ # Row color hooks
          utils/                    # Shared helper functions
      pages/                        # Generated (not modified)
      containers/                   # Generated (not modified)
      services/                     # Generated (not modified)
```

## Examples

### RackInspect
Single `GenericUser` actor with 87 custom files, 100+ Pandino registrations, 29 menu items, and no generated pages modified directly. Customizations include: dimension parameter system (custom visual element, 1,756 lines), VAT ID masking, exchange rate security, address auto-composition, table row highlighting, PDF preview, and getMask optimizations. All achieved through hooks without touching generated code.

## Trade-offs

- **Pros**: All pages benefit from generator updates; consistent page patterns; hook-based customization is non-invasive; single codebase to maintain
- **Cons**: Hook system has limits (some UI patterns require visual element override); large number of hooks can be hard to navigate; application-customizer grows very large
- **When to use**: Enterprise CRUD applications where the generated UI is adequate but needs significant behavioral customization

## Related Patterns

- [dual-actor-frontend-architecture](dual-actor-frontend-architecture.md)
- [application-customizer-hub](application-customizer-hub.md)
- [pandino-action-hook-override](pandino-action-hook-override.md)
- [zero-customization-generated-frontend](zero-customization-generated-frontend.md)

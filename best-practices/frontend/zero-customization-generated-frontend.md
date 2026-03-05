---
id: "zero-customization-generated-frontend"
title: "Zero-Customization Fully Generated Frontend"
domain: "frontend"
category: "framework"
score: 70.2
usage_count: 5
alternative_count: 2
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - itracker
  - skillmatrix-frontend
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
  - reserve-app
alternatives:
  - single-actor-heavy-customization
  - complete-frontend-replacement
---
## Description

A JUDO frontend where 100% of the UI is generated from the ESM model with no code-level customizations. No hook scaffolds are activated, no theme files are overridden, no custom components exist, and `.generator-ignore` contains only itself and `.gitignore` (React) or does not exist (Flutter). All UI behavior -- page layouts, field visibility, action buttons, confirmation dialogs, column widths, sort orders, and color palette -- is driven entirely by model-level configuration. This represents the fastest path to a working frontend: design the model, generate, deploy. Applies to both React and Flutter frontends. Flutter projects may still use Handlebars template overrides for cross-cutting features (download, upload, theming) without adding any hand-written Dart code.

## Structure

```
application/frontend-react/
  {model}__{actor}/
    .generator-ignore           # Only: .generator-ignore, .gitignore
    .gitignore                  # Lists all generated files
    public/
      logo.svg                  # Custom brand logo (only customization)
      i18n/                     # Generated translation files
    src/
      custom/
        application-customizer.tsx   # Generated scaffold (unmodified)
        hooks/
          containers/*.ts.default    # All inactive
          dialogs/*.ts.default       # All inactive
          pages/*.ts.default         # All inactive
      pages/                    # 100% generated
      containers/               # 100% generated
      dialogs/                  # 100% generated
      theme/                    # 100% generated from model colors
      layout/                   # 100% generated
      services/                 # 100% generated
```

Generator overrides directories exist but are empty (contain only `.gitignore`).

## Examples

### itracker
Two actor frontends (UserActor with 467 generated files, Admin with 277) both have zero customizations. UI richness is achieved through model configuration: 8+4 column split layout for Initiative view, conditional button visibility via derived booleans (`hideApproval`, `hideSendForApproval`), custom column widths (150-200px), custom sort orders (date ASC, timestamp DESC), 12-row page size for monthly forecast tables, `openInDialog` and `autoCloseOnSave` on sub-resource views, and branded colors via actor properties.

### SkillMatrix (Flutter)
Three Flutter actor frontends (Admin: 147 files, HR Employee: 1,093 files, Professional: 994 files) with zero hand-written Dart code. Only customization: 6 Handlebars template overrides for file download buttons on URL-type fields. All pages, stores, navigation, theming, and localization are 100% generated. The Professional actor manages dual roles (self-service + manager) entirely through model-defined page/route configuration.

### kozut-eugyfel-client (Flutter)
Three Flutter actor frontends (Munkatars: ~1,200 files, Admin: ~1,000, E-Ugyfel: ~330) with zero hand-written Dart code. No `custom/` folders, no `.generator-ignore` files. 12 Handlebars template overrides handle download/upload, custom theme palette, user widget with logo, and dependency management. All pages and stores are fully generated. Anonymous access for citizen portal entirely model-driven.

### kozut-eugyfel-model-test
Pure model project with zero frontend source code -- all UI is generated from the ESM model. The model defines 3 actors, 16+ entities, 7 enums, and bound operations that produce ~2,530 Dart files in the companion client with no hand-written code.

### reserve-app
Four of five actor frontends (PartnerActor, LogisticianActor, DoormanActor, Readonly) have zero code customizations. All `.generator-ignore` files contain only `.generator-ignore` and `.gitignore`. Three actors (Logistician, Doorman, Readonly) are dashboard-only placeholders with zero access points. PartnerActor has 2 access points (profile, reservations) but no hooks activated. All theme, layout, and i18n files are fully generated.

## Trade-offs

- **Pros**: Zero maintenance burden; all updates come from generator; fastest development cycle; model is the single source of truth; no merge conflicts on generated files
- **Cons**: UI flexibility limited to model capabilities; no custom business logic in frontend; standard look-and-feel; cannot implement advanced UX patterns (auto-scroll, masking, PDF preview)
- **When to use**: Internal tools, MVPs, prototypes, or applications where the standard JUDO CRUD UI meets all requirements

## Related Patterns

- [admin-default-generated-ui](admin-default-generated-ui.md)
- [model-defined-color-palette](model-defined-color-palette.md)
- [hook-scaffold-default-pattern](hook-scaffold-default-pattern.md)
- [single-actor-heavy-customization](single-actor-heavy-customization.md)
- [complete-frontend-replacement](complete-frontend-replacement.md)
- [flutter-frontend-framework](flutter-frontend-framework.md)

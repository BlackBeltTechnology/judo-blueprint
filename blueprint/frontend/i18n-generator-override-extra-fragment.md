---
id: "i18n-generator-override-extra-fragment"
title: "i18n Generator Override Extra Fragment for Custom Keys"
domain: "frontend"
category: "i18n"
score: 10.8
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
---
## Description

Inject custom translation keys into the generated default English translation file (`application_default.json`) using a Handlebars template fragment. The file `application_default_extra.fragment.hbs` is placed in `generator-overrides/ui-react/actor/public/i18n/` and its content is merged into the generated translations during code generation. This ensures custom keys have English defaults without modifying the generated file.

## Structure

```
application/frontend-react/
  generator-overrides/
    ui-react/
      actor/
        public/
          i18n/
            application_default_extra.fragment.hbs
```

Fragment content (JSON key-value pairs, no wrapping braces):
```
"extra.localization.operation.createCostPriceOperation": "Create CostPrice",
"custom.dialog.row-selection.title": "Select row from \"{{groupLabel}}\" group",
"custom.dimension.no-selection": "-- None --",
"judo.error.validation-failed.CUSTOM_ERROR": "Custom error message",
```

## Examples

### RackInspect
24 custom keys injected: operation labels (`extra.localization.operation.createCostPriceOperation`), dimension parameter UI text (`custom.dimension.*`), row selection dialog strings with `{{groupLabel}}` interpolation, picture creation label, and a custom validation error message. The corresponding Hungarian translations are maintained separately in `.generator-ignore`-protected `application_hu-HU.json`.

## Trade-offs

- **Pros**: Survives regeneration; generator handles merging; provides English defaults for all custom keys
- **Cons**: Fragment syntax must match generator expectations; Handlebars template expressions possible but rarely needed; must keep in sync with locale files
- **When to use**: Alongside any custom component that needs its own translation keys

## Related Patterns

- [i18n-custom-translation-keys](i18n-custom-translation-keys.md)
- [generator-override-extra-dependencies](generator-override-extra-dependencies.md)

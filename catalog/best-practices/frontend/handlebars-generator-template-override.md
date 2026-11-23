---
id: handlebars-generator-template-override
title: Handlebars Generator Template Override for Cross-Cutting Frontend Logic
description: Override specific Handlebars template fragments used by the JUDO code generator to inject custom logic into all generated frontend components that match a pattern.
aliases: [template override, hbs fragment override, cross-cutting generator override]
keywords: [handlebars, generator-overrides, fragment.hbs, template override, elementHasAnnotation, cross-cutting, OperationFlowManager, -DtemplateDebug]
tags: ["domain:frontend", "layer:frontend", "project:workflow-poc", "status:single-project"]
category: build
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: []
related: [operation-flow-redirect-pattern, generator-override-extra-dependencies, generator-ignore-app-theme]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Change what the generator emits for every component that uses a template or fragment, when the change cannot be made per page with hooks.

## Practice

### Platform base

- Templates are Handlebars (`.hbs`) files declared in a YAML descriptor. A same-named file in the override directory (`generator-overrides/`) is used instead of the default; the template name is shown in each generated file's header ([template override process](../../agent-docs/frontend/README.md)).
- Override layering: a same-name template with a new `templateName` or `pathExpression` replaces the original; a `<name>.override.hbs` decorates it and can include the original as a partial; `exclude: true` removes it. Fragment overrides work by creating a same-named file ([template variables](../../agent-docs/frontend/README.md)).
- Helpers come from the generator's helper classes (for example `toSafeCamelCase`, `firstToUpperCase`); run with `-DtemplateDebug` to see the context available in a template ([template variables](../../agent-docs/frontend/README.md)).
- The docs say to prefer hooks over overrides: you must maintain the template on every upgrade. For navigation after operations, the platform already offers `OperationFlowManager` ([OperationFlowManager](../../agent-docs/frontend/hooks/action-hooks.md)).

### Practice notes: an annotation-driven fragment

The example overrides the fragment that handles operation output, placing it under the override directory at the path the generator expects (here `ui-react/actor/src/fragments/operations/operation-primary-output-handler.fragment.hbs`). The fragment tests a model annotation and injects code:

```handlebars
{{# if (elementHasAnnotation operation.output.target 'redirect') }}
    await processRedirect(result);
{{/ if }}
```

`elementHasAnnotation` and the `operation.output.target` context come from one example project; they are not listed in the agent-docs, so confirm helper names with `-DtemplateDebug` on your generator version.

- Make the injected code conditional on an annotation, so only marked elements change.
- Inspect the generated output after each change: a wrong fragment breaks every page that uses it.
- Record why the override exists and re-check it at each platform upgrade.

## Rationale

One fragment reaches all generated places that use it, with no per-page hook code. The price is dependence on generator internals and upgrade upkeep.

## Example

One app: overrides `operation-primary-output-handler.fragment.hbs` so operation outputs annotated `@redirect` call `processRedirect(result)`. All of its operations (start, navigate, execute, assign) then route through its own flow manager rather than the default output dialog.

## When to avoid

- A hook, the `OperationFlowManager`, or a single-file `.generator-ignore` does the job: see [[generator-ignore-app-theme]] and [[operation-flow-redirect-pattern]].
- Only one page differs.
- The change is just extra dependencies: use [[generator-override-extra-dependencies]].

## Related

- [[operation-flow-redirect-pattern]] — the behavior this override feeds
- [[generator-override-extra-dependencies]] — simpler fragment use
- [[generator-ignore-app-theme]] — protecting single files instead

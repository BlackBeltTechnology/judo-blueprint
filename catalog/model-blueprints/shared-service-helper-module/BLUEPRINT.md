---
id: shared-service-helper-module
title: Shared Service Helper Module for Form Logic
description: "A frontend-only pattern for extracting shared form logic (field auto-computation, validation constraints, default initialization, and business rule application) into standalone TypeScript service modules under `src/custom/services/`."
aliases: [form logic module, hook helper functions, shared form helpers]
keywords: [shared, service, helper, module, form, logic, hook, storeDiff, typescript]
tags: ["domain:frontend", "layer:frontend", "project:park-here", "status:single-project"]
category: pattern
status: single-project
projects: [park-here]
evidence: ["park-here:unrecorded"]
alternatives: []
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Keep form business logic out of the generated-page hooks. Put the logic in plain TypeScript modules that several dialog and page hooks import. Each hook stays a thin wiring layer, and a rule that several forms share is written once.

### Hooks wire, modules decide

A form action hook only connects a callback (blur, after template load, option filter, validation props) to a function in the module. The function holds the rule.

### One module per input or domain concept

A module groups the functions for one input transfer object or one domain concept, for example the reservation form. A second module serves a second concept.

## Structure

The shape is a frontend source layout, not a model element.

- A module folder in the project's custom frontend code, one module per input or concept. The name `src/custom/services/<Name>Services.ts` is the project's convention, not a platform rule.
- Exported functions of the form `fn(data, storeDiff, ...extras)`. `data` is the form data, and `storeDiff(attribute, value)` writes a change into the form state. Hooks receive `data`, `editMode` and `storeDiff` from the generated hook interfaces. See [action hooks](../../agent-docs/frontend/hooks/action-hooks.md) and [data hooks](../../agent-docs/frontend/hooks/data-hooks.md).
- Hooks in different pages import the same module.

## Constraints

- The helpers are project code. The platform gives no registration for them; only the hooks that call them are registered, under the keys the framework generates for each page. See [[pandino-action-hook-override]].
- Helpers must not hold state between calls. Everything they need comes from `data` or the arguments.
- Helpers run in the browser and are a convenience. Server-side operations repeat every rule that matters.
- Async helpers (for example one that fetches a default) use the generated REST service client. See [[generated-service-layer-reuse]].

## Variations

- **Auto-computation.** Compute dependent fields, for example default start and end times from the current time.
- **Visibility by value.** Show or hide fields from an enumeration value. The flag name (`hiddenByCustom` in the source project) is that project's own attribute, not a platform name.
- **Template defaults.** Set defaults after the form template loads, from user preferences or related data.
- **Validation props.** Return min and max for date pickers.
- **Option filtering.** Narrow enumeration options by the user's permissions.
- **Warning text.** Show a message when a time is close to a boundary.
- **Relation defaults.** Fetch a default through the REST client, for example a preferred resource. Ask for the nested fields the helper needs in the same call with a mask.

## When to use

- Two or more hooks need the same form rule.
- A hook has grown long and mixes wiring with business rules.
- The rule needs a unit test without rendering a form.

## When to avoid

- One hook uses the logic once and it is short. Keep it in the hook.
- The rule belongs on the server (a validation or an interceptor). Put it there; see [interceptors](../../agent-docs/backend/interceptors.md).

## Related

- [[form-blur-action-hook]] — the hook that calls the helpers on field blur
- [[generated-service-layer-reuse]] — the REST client that async helpers use
- [[pandino-action-hook-override]] — how the hooks are registered
- [[reservation-booking-entity]] — the source project's reservation forms use such a module

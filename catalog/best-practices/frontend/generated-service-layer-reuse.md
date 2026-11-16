---
id: generated-service-layer-reuse
title: Reusing Generated TypeScript Service Layer in Custom UI
description: "When replacing the generated JUDO UI with a custom frontend, keep importing the generated TypeScript service implementations (Axios-based REST clients) and transfer object types instead of writing your own API layer."
aliases: [generated service reuse, judoAxiosProvider reuse]
keywords: [generated services, ServiceImpl, judoAxiosProvider, QueryCustomizer, transfer object types, custom UI, data-axios]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:actiongroup-test-react", "status:emerging"]
category: mapping
status: emerging
projects: [trivia, actiongroup-test-react]
evidence: ["trivia:unrecorded", "actiongroup-test-react:unrecorded"]
alternatives: []
related: [complete-frontend-replacement, error-code-mapping-pattern]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A custom UI should talk to the backend through the REST client code the generator already produces, so the API stays type-safe and follows model changes.

## Practice

### Platform base

- For each page and relation the generator emits services under `src/services/data-axios/`: `{Entity}ServiceImpl.ts` and `{Entity}ServiceFor{Relation}Impl.ts`. They are constructed with the generated `judoAxiosProvider` (`~/services/data-axios/JudoAxiosProvider`) ([service generation](../../agent-docs/frontend/model-screen-layout.md), [accessing generated services](../../agent-docs/frontend/development-workflow.md)).
- Because the services come from the UI model, regenerating after a model change updates them and the transfer object types together. Add the needed elements to the model's views instead of hand-writing replacements ([model features instead of custom components](../../agent-docs/frontend/ui-model-pitfalls.md)).

### Practice notes: use them from custom components

Instantiate the generated service once per component (for example with `useMemo`) and call its methods with generated types. The example also passes a `QueryCustomizer` with a `_mask` string to limit returned fields (see [[getmask-data-optimization]]).

```typescript
const orderService = useMemo(() => new OrderServiceImpl(judoAxiosProvider), []);
const [orders, setOrders] = useState<OrderStored[]>([]);

const data = await orderService.list(
  undefined,
  { _mask: '{number,total}' } as QueryCustomizer<Order>,
);
```

Names here are illustrative; the real class and method names derive from your UI model. Do not add the `src/services/` files to `.generator-ignore`; leave them regenerated.

## Rationale

The generated layer already handles transport, typing and the query customizer. Bypassing it duplicates that code and drifts from the backend after the next model change.

## Example

- A game frontend: four generated services created via `useMemo` (entry, listing and ranking, round flow, registration), all on `judoAxiosProvider`.
- A hand-built reference app: imports generated services directly for root CRUD, entity view, nested entity and many-aggregation access, plus the generated types and mask builders.

## When to avoid

There is no reason to bypass the generated layer inside a JUDO project. If a custom UI must run outside the generated build, consider whether the model should expose the data instead.

## Related

- [[complete-frontend-replacement]] — the custom SPA that reuses these services
- [[error-code-mapping-pattern]] — mapping backend errors the services return
- [[getmask-data-optimization]] — limiting fields with `_mask`

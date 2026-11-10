---
title: Generator Reserved Names
description: Member names that collide with generator-emitted methods and how to avoid them.
---

# Generator Reserved Names

**[◄ Back to Index](./README.md)**

Create and operation-input usage of a `TransferObjectType` (relations with the `createable` flag that target it, operations that take it as input) causes the generators to emit methods with fixed names. A relation or attribute whose `name` collides with one of these methods surfaces only at `tsgo` / `vite build` time as `error TS2393: Duplicate function implementation`, several transformation steps away from the root cause.

## Reserved Member Names

| Flag on TO | Emitted method | Reserved member name |
|---|---|---|
| the TO can be created through a relation (a `createable` relation targets it) or is the input of an operation | `getTemplate()` — returns a blank prototype for Create forms and operation forms (endpoint `<TO>/~template`; the REST client generator emits it when the TO `isTemplateable`). | **`template`** |

**Resolution:** rename the member and keep `binding` unchanged so the underlying entity relation is not disturbed (e.g. `name="template"` → `name="letterTemplate"`).

**Detection (before build):**

```bash
grep -nE 'createable="true"' model/*.model   # TOs at risk
grep -nE 'name="template"'   model/*.model   # candidate collisions
```

Any TO that appears in both results needs a rename.

## Related

- [Structure package](./structure.md) — `createable`/`updateable`/`deleteable` flags on `TransferObjectType`.

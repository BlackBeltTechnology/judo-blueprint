---
title: Generator Reserved Names
description: Member names that collide with generator-emitted methods and how to avoid them.
aliases: [reserved member names, template name collision, duplicate function implementation, TS2393 error, rename template member]
keywords: [getTemplate, template, createable, TransferObjectType, binding, isTemplateable, TS2393, letterTemplate, updateable, deleteable]
tags: [domain:model, layer:model, status:platform]
---

# Generator Reserved Names

**[◄ Back to Index](./README.md)**

Create and operation-input usage of a `TransferObjectType` (relations with the `createable` flag that target it, operations that take it as input) causes the generators to emit methods with fixed names. A relation or attribute whose `name` collides with one of these methods surfaces only at `tsgo` / `vite build` time as `error TS2393: Duplicate function implementation`, several transformation steps away from the root cause.

## Reserved Member Names

| Flag on TO | Emitted method | Reserved member name |
|---|---|---|
| the TO can be created through a relation (a `createable` relation targets it) or is the input of an operation | `getTemplate()` — returns a blank prototype for Create forms and operation forms (endpoint `<TO>/~template`; the REST client generator emits it when the TO `isTemplateable`). | **`template`** |

**Resolution:** rename the member and keep `binding` unchanged so the underlying entity relation is not disturbed (e.g. `name="template"` → `name="letterTemplate"`).

### Detection (before build)

```bash
grep -nE 'createable="true"' model/*.model   # TOs at risk
grep -nE 'name="template"'   model/*.model   # candidate collisions
```

Any TO that appears in both results needs a rename.

### Java reserved words

`safeName()` appends an underscore to a name that is a Java reserved word (including `class`, `Class`, `int`, `interface`, `default`): `class` becomes `class_` (a suffix, not a prefix).

### Generated database name limits

Generated table and column names are abbreviated to a maximum length. The defaults are 62 characters for tables and 58 for columns on HSQLDB and PostgreSQL, and 30 for both on Oracle; `tableNameMaxSize` and `columnNameMaxSize` override them.

## Related

- [Structure package](./structure.md) — `createable`/`updateable`/`deleteable` flags on `TransferObjectType`.

---
title: Operation Script Language (JCL)
description: Syntax, restrictions and validation of JCL operation body scripts in JUDO models.
aliases: [jcl script, operation script language, script functions, parameterized query script, operation body script, script validation]
keywords: [JCL, ACTOR, JQL, validation, operation body]
tags: [domain:model, layer:model, status:platform]
---

# Operation Script Language (JCL)

> **Deprecated:** JCL is deprecated. Prefer `customImplementation = true` with a Java implementation for new operations.

JCL (JUDO Control Language) is the imperative language of operation bodies. An operation whose `customImplementation` is `false` carries a JCL script in its `body`; `customImplementation = true` switches the operation to a Java implementation instead (see [operation.md](./esm_metamodel/operation.md)). JQL expressions (see the JQL reference in [model-development.md](./model-development.md)) are used inside the statements, but scripts have their own rules and restrictions, described here.

## Statements and syntax

- **Statement terminators** (`;`) are optional.
- **Declarations**: `var [immutable|mutable] Type [[]] name [= initializer]`. Variables can only be declared inside blocks, and shadowing a variable of an outer scope is forbidden (`Variable <name> already defined`). The loop variable of a `for` statement is final.
- **Control flow**: `if (cond) stmt [else stmt]`, `for (x in <collection>) stmt`, `while (cond) stmt`, `return [value]`, and blocks `{ ... }`.
- **Creating objects**: `new [mutable|immutable] Type(...)` takes either a single assignable value or named assignments, and must list every required attribute and relation. `new Type[] { a, b }` creates several at once.
- **Removing**: `delete <navigation>` removes composition parts; `unset <navigation>` clears a reference.
- **Reference sets** are changed with `+=` (add) and `-=` (remove).
- **Subtype spawning**: `x as Type` casts a transfer object reference to a subtype. A wrong runtime type is a runtime error; an incompatible static type is a compile-time error. Spawning is only allowed on mutable, assignable operands (`Cannot spawn immutable objects`).
- **Unary prefix operators** are `not`, `-`, `mutable` and `immutable`.
- **The instance is `this`, not `self`**: in an instance operation body the current object is `this` (`this.status = ...`). `self` is the JQL name used in derived expressions; in a JCL body it fails the build with `Unknown symbol: self`.
- **Operation calls**: the parenthesis must follow the feature name immediately, with no whitespace (`this.a(this.b())`).
- **No dangling navigation**: a bare navigation used as a statement is an error (`Dangling navigation`); a statement must be a call, an assignment or another real statement.
- **Naming**: the operation's input parameter is called `input` and is immutable unless declared mutable; the implicit return value is called `output`. Only the first argument of an operation call is bound; later arguments are silently dropped.
- **Immutability**: `mutable`/`immutable` is a JCL concept, not an ESM attribute of references. Everything read from an operation's `input` is immutable, and navigating from an immutable object (including a transient reference of the input) stays immutable. On an immutable object, a bound operation call fails (`Cannot call operation on immutable object`), `as Type` fails (`Cannot spawn immutable objects`), `return` of it fails (`Cannot return with immutable object.`), assigning it into mutable state fails (`Invalid operation with immutable object`), and changing a collection through it fails (`Immutable selector`). Create a mutable copy with `new mutable Type(...)` to modify data.
- **No fault or service statement**: a script has no statement to raise a modeled fault and no way to call an OSGi service: the statements are declaration, call, `return`, `unset`, `delete`, `create`, block, `if`, `for` and `while`. Implement the operation in Java (a custom implementation) when it must throw a modeled fault or use a service. *Verify:* whether a fault raised by an operation that the script calls reaches the caller unchanged.
- **Code generation**: the generated Java method body is built from the first script block only; other blocks are ignored. A `delete` statement generates a call to `super.deleteElement(...)` on the referenced object (once per element for a collection), not a direct DAO delete.

## Authenticated actor in scripts

Inside scripts the current actor is available through the script functions `principal` and `iscurrentactor`, and a leading navigation name that resolves to an actor type becomes an actor reference rather than a data navigation. This is separate from the `!getVariable('ACTOR' | 'PRINCIPAL' | 'USER', ...)` claim lookups described in [advanced-modeling-patterns.md](./advanced-modeling-patterns.md).

## Functions that differ from JQL

- The operators `typeOf`, `kindOf`, `asType`, `asCollection` and `container` are **not supported in scripts**: they throw `<name> is not supported in scripts`, although the JQL reference lists them.
- Available script functions include the object selectors `head`, `tail`, `heads` and `tails` (with `asc`/`desc`), `getVariable`, `isAssignable`, `principal` and `iscurrentactor`.

## Parameterized queries in scripts

A derived feature that takes an input transfer object is a *parameterized query*, marked by a `parameterized` extension annotation (`true`). A call dispatches in this order: operation, primitive parameterized query, complex parameterized query. Primitive query calls are typed by their result (`Integer`, `Decimal`, `Boolean`, `String`, enumeration, custom type, `Date`, `Time`, `Timestamp`). Static calls of the form `TypeName#query(...)` are only allowed on **unmapped** transfer objects (`Static parameterized query calls are only supported on unmapped transferobjects`), and a missing input is a build error (`Query input parameter cannot be empty`).

## Validation

The editor validator `ScriptValid` (EVL constraint, ERROR) builds every non-custom operation body and reports the JCL validator's message; operations with `customImplementation = true` are skipped, so their Java body is never parsed by the editor. See also [Model validation](model-validation-and-transformation.md).

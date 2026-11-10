---
id: sequence-code-generation
title: Sequence-Based Code Generation in Java
description: "A custom operation takes the next number of a named platform sequence from the VariableResolver (category SEQUENCE) and formats it into a padded code such as PRT-00001."
aliases: [sequential codes, padded number generator, SEQUENCE variable]
keywords: [sequence, variable resolver, code generation, padded number, prefix, counter]
tags: ["domain:backend", "layer:backend", "project:judo-partner", "status:single-project"]
category: service
status: single-project
projects: [judo-partner]
evidence: ["judo-partner:unrecorded"]
alternatives: [sequence-based-identifier]
related: [actor-resolution-variable-resolver, builder-pattern-entity-creation, sequence-based-identifier, document-registry-sequence]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An entity needs a short, human-readable, increasing code (`PRT-00001`) that the user does not type. When the code depends on logic only Java has (a prefix per register, a format that varies by data), the custom operation asks the platform for the next value of a named sequence and formats it itself.

## Practice

### Platform base

- `SEQUENCE` is one of the variable categories the platform resolves, next to actor and principal variables; the same `VariableResolver` serves them ([custom operations](../../agent-docs/backend/custom-operations.md), [reading the principal and actor](../../agent-docs/backend/interceptors.md#reading-the-principal-and-actor-in-an-interceptor)).
- Sequences are database sequences by default (`sequenceType` `rdbms`). A custom implementation of the platform `Sequence` interface can replace them; transient sequences are not supported on multi-node deployments ([custom sequences](../../agent-docs/backend/platform-behavior-reference.md#custom-sequences)).
- Sequences can have gaps: values of rolled-back transactions are not reused (same section). A code is unique and increasing, not gap-free.
- Components that are bound to one model carry the `judo.model.name` property ([interceptor registration](../../agent-docs/backend/interceptors.md#interceptor-component-registration)). The agent-docs do not say whether `VariableResolver` needs a model-name target filter; the project below used one.
- When the number is only a stored attribute with a default, the model can do it without Java, see [[sequence-based-identifier]].

### Project practice: format in Java

This layer is project practice (judo-partner), not a platform feature:

- One sequence name per number space. A fixed name (`partner`) for one entity, or a dynamic name (the register code) when each register counts on its own.
- Pad with `String.format("%05d", n)`; the width is fixed, larger numbers simply get longer.
- Request the number once per created entity, in the same operation that creates it, so a failed operation does not hand out the code to anything else (the consumed number is still lost, which only causes a gap).
- Do not compute the next code from a count or a max query: concurrent creates collide.

```java
// Example project code: the model name filter and the sequence names are project choices
@Reference(target = "(judo.model.name=AppName)")
VariableResolver variableResolver;

String code = String.format("PRT-%05d",
    variableResolver.resolve(Long.class, "SEQUENCE", "partner").intValue());
// PRT-00001, PRT-00002, ...

String recordNumber = String.format("%s-%05d",
    register.getRegisterCode(),
    variableResolver.resolve(Long.class, "SEQUENCE", register.getRegisterCode()).intValue());
```

## Rationale

- The database owns ordering and uniqueness; application code only formats.
- Independent sequence names allow independent number spaces without extra tables.
- Calling the resolver in Java allows a prefix or format that depends on data at runtime.

## Example

In judo-partner two sequences are used. The partner service builds partner codes `PRT-XXXXX` from the sequence named `partner`. The register service builds record numbers from a sequence named after the register's code, so each register numbers its records independently. Both use five-digit zero padding.

## When to avoid

- The code is a plain stored attribute: use a default expression in the model ([[sequence-based-identifier]]).
- Numbers must be gap-free or reset per period: sequences have gaps and no reset; see [[document-registry-sequence]] for a registry design.
- `intValue()` on a `Long` overflows past about two billion; use the long value if the space is large.

## Related

- [[sequence-based-identifier]] — the model-level default-expression variant
- [[document-registry-sequence]] — registry numbering with prefix and period
- [[actor-resolution-variable-resolver]] — the same resolver for actor lookups
- [[builder-pattern-entity-creation]] — creating the entity that carries the code

---
title: Model Documentation
description: Model documentation for JUDO applications: ESM metamodel, JUDO Model CLI, JQL, modeling patterns, validation and transformation.
aliases: [model documentation index, how to change the model, model CLI, modeling guide, cardinality meaning, CRUD flags, which model doc to read]
keywords: [judo-cli.jar, merge, esm.ecore, JQL, createable, updateable, deleteable, 0..1, 1..*, Designer]
tags: [domain:model, layer:model, status:platform]
---

# Model Documentation

This directory contains documentation related to the application's domain model.

## Model Design & Development

Model elements (entities, attributes, relations, operations) are created and changed with the [JUDO Model CLI](judo-cli.md) or the Designer; never by editing the model XMI as text.

**Key principle:** a model is changed by exactly one writer at a time; parallel work uses separate copies joined with the CLI `merge` command (see [judo-cli.md](judo-cli.md)).

## Reference Documentation

- **[JUDO Model CLI](judo-cli.md)**: The `judo-cli.jar` platform tool — the only sanctioned way to read or change the ESM. **Read this first if you have not used the CLI before.**
- **[Transformation Pipeline](transformation-pipeline.md)**: ESM → PSM → ASM → RDBMS → Liquibase, server-side vs client-side regeneration, and the in-memory state model.
- **[Model Development Guide](model-development.md)**: Modeling workflow, naming conventions, and **JQL expression language reference**.
- **[UI Authoring Guide](ui-authoring-guide.md)**: How to compose `<form>`, `<table>`, `<view>` scaffolds on `TransferObjectType`s and wire them onto an `ActorType` menu. **Read this before authoring UI elements.**
- **[Advanced Modeling Patterns](advanced-modeling-patterns.md)**: Reusable design patterns for common modeling problems.
- **[Generalization Guide](generalization-guide.md)**: Entity inheritance and generalization patterns.
- **[XMI ID Traceability](xmi-id-traceability.md)**: How JUDO maintains traceability from model elements to generated artifacts.
- **[Operation Script Language (JCL)](jcl-operation-scripts.md)**: Syntax and restrictions of operation bodies.
- **[JSL Language Rules](jsl-language-notes.md)**: Identifiers, built-in libraries, actor grammar and the rules that fail a build.
- **[Validation and Transformation Options](model-validation-and-transformation.md)**: EVL validation, ETL vs ZETA engines, Maven workflow, measures, known issues.
- **[ESM Metamodel](./esm_metamodel/README.md)**: Detailed breakdown of every component in `esm.ecore`.

## Quick Reference

### Cardinality

| Cardinality | Meaning | Example |
|-------------|---------|---------|
| `1..1` | Required single | `order: Order` (must have exactly one) |
| `0..1` | Optional single | `logo: Image` (zero or one) |
| `0..*` | Optional many | `participants: User[]` (zero or more) |
| `1..*` | Required many | `items: OrderItem[]` (at least one) |

### CRUD Flags

| Flag | Purpose |
|------|---------|
| `createable` | Entity instances can be created |
| `updateable` | Entity instances can be modified |
| `deleteable` | Entity instances can be deleted |

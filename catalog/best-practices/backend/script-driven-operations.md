---
id: script-driven-operations
title: Script-Driven Operations (No Custom Java)
description: "Business logic is written as JCL scripts in the operation bodies of the model (customImplementation false), so the build generates the operations and no Java implementation classes are written."
aliases: [JCL operations, model scripts, zero custom java]
keywords: [script, JCL, operation body, customImplementation, no custom java, model-driven, init]
tags: ["domain:backend", "layer:backend", "project:itracker", "project:viterra_demo", "project:judo-demo-miniworkflow", "project:reserve-app", "project:doors-model", "status:established"]
category: operation
status: established
projects: [itracker, viterra_demo, judo-demo-miniworkflow, reserve-app, doors-model]
evidence: ["itracker:unrecorded", "viterra_demo:unrecorded", "judo-demo-miniworkflow:unrecorded", "reserve-app:unrecorded", "doors-model:unrecorded"]
alternatives: [custom-operation-osgi-component]
related: [custom-operation-osgi-component, state-lifecycle-operation, init-data-seeding, interceptor-crud-lifecycle]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Most operations of a business application only change a status, create a few related rows or aggregate a collection. The model can carry that logic itself: an operation with `customImplementation = false` has a JCL script as its body, and the build generates the runtime operation from it. No `*CustomImplementation` Java class exists for these operations, so the model stays the single source of truth.

## Practice

### Platform base

- `customImplementation = false` means the body is a JCL script and the implementation may be generated; `true` switches to a Java implementation and the body is only documentation ([operation metamodel](../../agent-docs/model/esm_metamodel/operation.md), [JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md)). In the transformation pipeline the scripts go through `asm2script` and `script2operation` ([transformation pipeline](../../agent-docs/model/transformation-pipeline.md)).
- Script syntax: optional `;`, typed `var` declarations inside blocks, `if`, `for (x in collection)`, `while`, `return`; `new Type(...)` with every required attribute and relation; `delete` and `unset`; `+=` and `-=` on reference sets. The operation input is called `input`, the return value `output`. The actor is available through the script functions `principal` and `iscurrentactor`. `typeOf`, `kindOf`, `asType`, `asCollection` and `container` are not supported in scripts ([JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md)).
- The editor validates every non-custom operation body (`ScriptValid`, error severity), so a broken script is caught at model validation, not at runtime. Operations with a Java implementation are skipped by that check.
- Script operations never hit interceptors. Interceptors fire only for built-in behaviour operations, and custom, mapped and script operations bypass them. Permission checks that matter must be expressed in the script or in the model's access rules ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- The agent-docs describe no way for a script to call an OSGi service, a SOAP/REST client or a mail sender, nor to raise a modeled fault. Treat anything that needs them as a Java custom operation ([custom operations](../../agent-docs/backend/custom-operations.md)) and test before relying on a script for it.

### Practice notes: scripts as the only implementation

This layer is a convention built on the platform, not a platform feature:

- Use scripts for status transitions, entity creation with child rows, versioning with collection aggregation, and seeding reference data in an init operation ([[state-lifecycle-operation]], [[init-data-seeding]]).
- Keep a Java custom implementation only for operations that truly need Java: file handling, document templating, external services. Mark exactly those `customImplementation = true`.
- Document the intended behaviour in the operation's doc comment; the stub generated beside an unused custom class then shows what the script does.
- Make init scripts idempotent, for example with a stored migration counter that records which seed steps already ran.
- Where the only Java needed is cross-cutting (statistics, tracking), use interceptors for built-in operations and keep the operations themselves scripts.

```
// Example JCL-style statements, shape only (see the JCL guide for exact syntax)
this.status = Status#REVIEW                       // status transition
var item = new Item(title = input.title)           // entity creation
this.children += new Child(month = 0, value = input.value)   // add to a reference set
```

## Rationale

- No Java to maintain for plain state changes, and a logic change is a model change.
- The model validator checks the script, so errors surface early.
- The cost is expressiveness: no external integration and little room for fine-grained error handling, and a compiled script is harder to debug than Java.

## Example

- One application: all operations (create, send for approval, approve, reject, archive plan at actor and entity level) plus init are scripts. They create a plan with monthly entries and version plans with collection aggregation.
- One example: report lifecycle (accept, review, submit) and init data are scripts.
- A demo: document workflow transitions, creation with owner and first history entry, and idempotent user seeding are scripts.
- One application: one script operation (user init, `customImplementation` false); all Java customization is interceptors.
- One application: many operations in the expression language (approval start, next-stage state machine with skip/execute conditions by net value, approve/reject, init with a migration counter). Only a few operations that need Java (file handling, document templating) are custom.

## When to avoid

- The operation calls an external service (mail, file store, SOAP, REST, identity provider).
- It needs fine-grained error handling or modeled faults whose script support you have not verified.
- It needs a permission check that the model's access rules cannot express: interceptors will not help here, so use a Java operation with the check inside.

## Related

- [[custom-operation-osgi-component]] — the Java alternative with injected DAOs and services
- [[state-lifecycle-operation]] — status transitions, often written as scripts
- [[init-data-seeding]] — seeding in an init operation
- [[interceptor-crud-lifecycle]] — Java customization for built-in operations beside script operations

# Applying a catalog entry

## Blueprints

1. Read `BLUEPRINT.md`: *Intent*, *Constraints*, *Variations*, *When to avoid*. Pick the variation that fits.
2. Read `model.md`. `## Model shape` lists the elements; the generated Mermaid diagram shows the structure. The diagram is derived from a validated fragment model (`fragments/<id>.model` in the catalog repo), so the shape is known to pass strict validation.
3. Rename to your domain. Entry names are neutral examples (`Partner`, `Order`); keep the relation kinds, cardinalities, flags and expressions.
4. Build it with the JUDO model CLI skill in your project (one writer per model file), then `validate --strict`.
5. Read `backend.md` and `frontend.md` only for the layers you touch. Code there is **example project code** unless it says *platform*: adapt it, do not copy class names that do not exist in your project.

## Best practices

Read *Practice* and *Example*. The *Rationale* says why; *When to avoid* says when not to. Follow the links into `agent-docs/` for the platform rule behind it.

## Platform vs project practice

Entries separate the two:

- **Platform**: behaviour of the generated code and runtime, backed by `agent-docs/`. Rely on it.
- **Project practice**: what one or more projects chose. Adopt it if it fits; it is not enforced by the platform.
- **Verify** notes mark claims the agent-docs do not settle (for example the transaction scope of a custom operation). Test them in your project before relying on them.

## Known platform pitfalls

- Interceptors run only around built-in operations, never around custom, mapped or script operations.
- An actor access target must be a mapped transfer object.
- JCL operation bodies use `this`; `self` is JQL only.
- A business error is a modeled fault declared on the operation (422). A bare `RuntimeException` becomes a 500.
- `judo-cli` cannot set `relationKind=AGGREGATION`; use `ASSOCIATION` or `COMPOSITION`.

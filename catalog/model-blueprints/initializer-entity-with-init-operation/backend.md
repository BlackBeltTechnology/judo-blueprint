## Backend guidance

Platform facts: an initializer operation is a static operation with an initializer flag and no input. Built-in operations and their interceptors do not apply to custom operations. Types such as `InitializerContext` and the helper methods below are illustrative application code, not platform API.

### Implement init as a custom static operation

The init operation is a custom operation, so the backend provides its body. Interceptors do not run for custom operations, so `init` gets no interceptor around it. Put any logging or audit inside `init`.

```java
public static void init(InitializerContext context) {
    if (context.referenceDataExists()) {
        return; // guard: safe to run on every start
    }
    context.seedReferenceData();
}
```

### Guard against repeated runs

Choose one guard and document it:

- check whether the seed data already exists before writing it,
- set the `createdAt` marker last, after every write has succeeded, and return early when it is set,
- or keep a counter and run only the numbered steps that are not yet recorded.

### Keep the seed inside one transaction

Write all seed rows in the operation's transaction. A failure then rolls back the whole seed, and the next start retries it cleanly.

### Use application services for lookups

Seed code that looks up existing rows usually calls application services. Those services are application code, not platform API, so copy the pattern and not the names.

## Examples

### Variant seen in practice

- The init operation seeds cities, postal codes, capabilities, the platform configuration singleton, and an admin organization with an admin user.
- It runs with the `createdAt` marker set last.

### Second variant seen in practice

- The init operation runs numbered migration steps in order. A counter attribute records the last completed step, so each step runs once across deployments.
- A gap in the step numbers marks a step that was removed.

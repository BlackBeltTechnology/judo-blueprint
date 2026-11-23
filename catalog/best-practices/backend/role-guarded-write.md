---
id: role-guarded-write
title: Role-Grouped Write Guards with a Model-Derived Coverage Test
description: "Write interceptors grouped by verb and permitted roles list their operations by name, a coverage test derived from the model fails on any unguarded write, and a central guard service adds row-level ownership and state checks."
aliases: [write guard, role write guard, write coverage test, row-level guard service]
keywords: [write guard, OperationCallInterceptor, role, permission, coverage test, fail closed, ownership, state guard, guard service]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: auth
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/access/WriteGuards.java", "rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/access/update/PriceModifierUpdateGuard.java"]
alternatives: []
related: [role-based-invitation-guard, guarded-delete-with-deactivate-fallback, interceptor-security-filter-validation, typed-exception-error-handling]
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

Who may write what is a security rule, and a rule written as a free-form interceptor per entity is easy to leave incomplete: a write that nobody lists is simply unguarded, with no error and no log line. This practice states the rule as a small number of guards, each one a set of write operations plus the roles allowed to perform them, and adds a test that derives the full set of write operations from the model and fails when any has no guard. A second level, a central guard service, handles what a role list cannot: ownership and state of the row being written.

## Practice

### Platform base

- A write guard is an `OperationCallInterceptor` registered as an OSGi component with `judo.model.name=<app>`; `getOperations(AsmModel)` returns the operations it covers, and an empty collection means all built-in operations ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)).
- Interceptors fire **only for built-in behaviour operations** (create, update, delete, set/unset/add/remove reference and so on). Custom, mapped and script operations never reach them, so guards for those go inside each `*CustomImplementation` ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted), [custom operations](../../agent-docs/backend/custom-operations.md)).
- Operation names are fully qualified, for example `<app>.<package>.<Actor>#_createInstance<Relation>`; the verb is visible in the `_createInstance`, `_updateInstance`, `_deleteInstance`, `_setReference` and similar prefixes ([operation FQN format](../../agent-docs/backend/interceptors.md#operation-fqn-format-reference)).
- A refusal is `InterceptorCallBusinessException` with your own stable error code; it answers HTTP 422 and rolls back the operation's transaction ([throwing a business error](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).
- Declarative Services does not inherit references: collaborators held in a shared base class produce no references in the component descriptor. Whether this applies to your build, check the generated `OSGI-INF` descriptors (*verify*).
- A modeled `hiddenBy` only hides UI. It does not protect the operation.

### Practice notes: guards grouped by role

This layer is a convention built on the platform, not a platform feature:

- **One contract, two answers.** A `WriteGuard` interface extends the interceptor and asks an implementation for just two things: `operations()` (fully qualified names) and `permitted()` (a set of roles). The name, the resolution of names to operations and the refusal are shared. A guard is then readable as a statement of policy.
- **One guard per verb and role set**, in one package per verb (`create`, `update`, `delete`), so "what may this role delete?" is answered by one folder. A guard that belongs to a feature package may declare its verb explicitly.
- **Shared static helper, not a base class**, for the same Declarative Services reason. Each guard repeats its few `@Reference` fields and an explicit `service = OperationCallInterceptor.class`.
- **Resolve strictly.** An unresolvable name, or an empty list, throws instead of skipping. Resolution is lazy, so the failure shows on the first dispatched call, not at activation. Cache the resolved set per guard and per model, because the dispatcher asks for operations twice per call for every registered interceptor, and key the cache on the model so a second model cannot silently match nothing.
- **Fail closed.** If the caller cannot be identified, refuse, and log it so an infrastructure failure is not read as "no permission". Use the narrow wording ("only an administrator may...") only when the permitted set really is that narrow.
- **One registry list.** A `WriteGuards.ALL` list names every guard class. The runtime finds guards without it; it exists so completeness can be checked.
- **Reach versus write.** Keep a separate grid of which roles can reach each area, and assert at guard start that a role never writes an area it cannot reach.

### The coverage test

The hand-written lists are safe only because a test proves them complete:

- Derive the set of write operations from the model: every create, update, delete and reference write on the actor's accesses, with an explicit, named exclusion list for nested data no access targets.
- Assert that the union of all guards' operations equals that set. A write with no guard fails, and so does a guard naming an operation that is not a write.
- Assert that each name resolves in the model, so the exclusion constants cannot rot.
- Keep a second, independent transcription of the role grid in test code and assert that it equals the production one. Two copies catch a drift that one shared constant hides.

Deleting this test returns the design to the bug it replaced.

### Second level: row-level ownership and state guards

A role list says who may write an area, not which row. Put that in one injectable guard service that every operation body calls before it writes:

- **Role guards read a model attribute.** A derived, actor-scoped flag on the bound instance (for example "actor cannot manage this") is evaluated by the dispatcher when the instance is loaded. The guard refuses on `true`, on empty and on absent, so the role set lives in one place, the model, and no Java copy can drift.
- **Ownership guards** compare the caller's own scope (for example the account the user belongs to) with the scope of the row, and refuse when they differ.
- **State guards** read the row's derived gate attribute instead of re-deriving the rule in Java, so each guard is the exact negation of its gate by construction. Re-read the bound instance through the DAO before guarding, because gates are only populated on a fully masked read, and treat an absent gate as a refusal.
- **Stable error codes per guard family**, derived from the gate names so guard, gate and code move together; tests assert the constant, never a literal. The guard service resolves messages from an i18n service in the request locale.
- Operation bodies call the service first. Because custom operations are not intercepted, this is where their guard lives; for built-in writes the same service can be called from the interceptor.

```java
// Example code: names are illustrative
public interface WriteGuard extends OperationCallInterceptor {
    List<String> operations();   // fully qualified operation names, one verb
    Set<ActorRole> permitted();  // roles allowed to perform them
}

@Component(service = OperationCallInterceptor.class, property = { "judo.model.name=app" })
public class AccountCreateGuard implements WriteGuard {
    @Reference ActorService actorService;
    @Reference AppI18n i18n;
    @Reference ThreadLocalLocaleSupplier localeSupplier;

    public Set<ActorRole> permitted() { return Set.of(ActorRole.ADMIN, ActorRole.MANAGER); }
    public List<String> operations() { return List.of("app.services.GenericUser#_createInstanceAccounts"); }

    @Override
    public Object preCall(EOperation operation, Object payload) throws InterceptorCallBusinessException {
        WriteGuardSupport.requirePermitted(this, actorService, i18n, localeSupplier);
        return payload;
    }
}

// operation body, row level
guardService.requireTicketingRole(Optional.ofNullable(_this.getActorCannotManageTicket()));
guardService.requireTicketEditable(ticket);
```

## Rationale

- Grouping by verb and role set keeps the number of guards small and each one reviewable on one screen.
- Listing names by hand costs nothing at runtime; the coverage test removes the one risk of doing so.
- A guard that covers nothing looks like a fix, so strict resolution and the empty-list failure make mistakes loud.
- Row-level rules from model-derived flags keep one source of truth per rule, and the UI gate and the server guard cannot disagree.

## Example

Around a dozen guards cover create, update and delete across the actor's areas, split by role set (administrator-only, a supplier-side role, a role for price data, an external reviewer panel, user management with row-level checks). The coverage test derives write operations from the model and was added after an earlier design guarded only a few areas while looking finished. The operation bodies of one capability call a guard service that checks the role flag, the caller's account against the row's account, and each state gate, with a separate error code per family.

## When to avoid

- A single, rarely changing rule on one entity: a guard class plus a registry plus a coverage test is more machinery than a check in one operation body.
- Rules that change at runtime or per tenant: keep them in data, not in role lists in Java.
- Read visibility: model it with accesses and `hiddenBy`, and use a range interceptor for exposed relations, not a write guard.

## Related

- [[role-based-invitation-guard]] — the same deny-by-default role check, written inside one custom operation
- [[guarded-delete-with-deactivate-fallback]] — a row-level delete guard that fails loudly and steers to deactivation
- [[interceptor-security-filter-validation]] — interceptor-level security checks
- [[typed-exception-error-handling]] — how business refusals are shaped

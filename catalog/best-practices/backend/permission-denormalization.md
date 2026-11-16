---
id: permission-denormalization
title: Permission Denormalization from Role Assignments
description: Practice that copies the permission flags of a user's roles onto boolean attributes of the user entity, recalculated by a custom operation that interceptors trigger when roles or assignments change.
aliases: [denormalized permissions, permission flags on user, role to boolean flags]
keywords: [permission, denormalization, role, flags, recalculate, interceptor, boolean, user, admin guard]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: auth
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/user/roles/UserRolesChangeInterceptor.java"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Make permission checks a single boolean read. Instead of joining user, roles and permissions at query time, the flags granted by a user's roles are stored as boolean attributes on the user entity and recalculated whenever roles change. This is a convention built on the platform; the platform provides the hooks it relies on but no such feature.

## Practice

### Platform: the pieces the pattern uses

- Interceptors fire only for the built-in behaviour operations (create, update, delete, set/unset/add/remove reference and so on). Custom, MAPPED and script operations never hit interceptors, so permission checks for custom operations must sit inside each `*CustomImplementation` ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). The recalculation is triggered from interceptors on the built-in role and role-assignment operations; it does not guard any custom operation by itself.
- Authorization belongs in the model's access control where possible; the stored flags are readable from access filters and expressions through the actor variables ([ACTOR vs PRINCIPAL vs USER](../../agent-docs/model/advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables)). Which variable category applies depends on the actor shape; a wrong attribute name yields empty results silently.
- The update call is the plain DAO update, with a mask limiting the written fields ([mutable entity update](../../agent-docs/backend/data-access-guide.md#using-masks-projections)).

### Practice notes: recalculate flags from roles

- The user entity carries one boolean per permission (a fixed set of flags, for example for data, roles, users and orders). A permission enumeration lists the flags; roles hold a set of permissions.
- A custom `RecalculatePermissions` operation (example code) collects the permission values of all roles assigned to the user and sets each boolean:

```java
// Example code: User, Role, PermissionFlag and the DAOs are generated types
Set<PermissionFlag> flags = new HashSet<>();
for (Role role : userDao.queryRoles(user).selectList()) {
    flags.addAll(roleDao.queryPermissions(role).selectList().stream()
        .map(Permission::getPermissionFlag).toList());
}
Map<String, Object> before = new HashMap<>(user.toMap());
user.setCanManageUsers(flags.contains(PermissionFlag.USERS));
user.setCanManageRoles(flags.contains(PermissionFlag.ROLES));
// ... one setter per flag
if (!before.equals(user.toMap())) {
    userDao.update(user, UserMask.userMask());
}
```

- Two interceptors keep the flags current: one on role permission changes recalculates all users; one on assigning or removing roles for a user recalculates only that user.
- A guard in the same interceptors refuses a change that would leave nobody with both the roles and users permissions.
- The write is skipped when nothing changed ([[dirty-check-before-update]]).

## Rationale

- Permission checks and model access expressions read one boolean per flag; no join at query time.
- The flags can be used directly in access filters and UI bindings.
- Costs: a role change recalculates every user (linear in the user count), the user entity grows wide, and the copy drifts if a change path bypasses the interceptors (for example a custom operation or direct data load that edits roles, since interceptors do not fire for those).

## Example

A role that holds the roles and users permissions is removed from the last administrator: the role interceptor detects that no other user would keep both permissions and rejects the change. When a role gets a new permission, every user holding that role gets the new boolean set on the next recalculation pass.

## When to avoid

- When a derived boolean on the user can compute the flag from the roles on read; it cannot drift ([[derived-attribute-flattening]]).
- When roles come from the identity provider and the application does not manage them itself.
- When the user count is large and roles change often; the full recalculation becomes expensive.

## Related

- [[interceptor-crud-lifecycle]] — the interceptors on role and assignment changes
- [[dirty-check-before-update]] — avoids writing unchanged users
- [[derived-attribute-flattening]] — compute-on-read alternative
- [[user-with-role-permission-entity]] — the model shape of users, roles and permissions

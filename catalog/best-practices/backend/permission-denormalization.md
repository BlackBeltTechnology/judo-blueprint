---
id: permission-denormalization
title: Permission Denormalization from Role Assignments
description: A role-based permission system where permission flags are denormalized onto the User entity as individual boolean fields.
aliases: []
keywords: [permission, denormalization, from, role, assignments]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: auth
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
related: [interceptor-crud-lifecycle, dirty-check-before-update]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

A role-based permission system where permission flags are denormalized onto the User entity as individual boolean fields. When roles or role-permission mappings change, a `RecalculatePermissions` operation collects all PermissionFlag enum values from the user's assigned roles and sets 20+ boolean fields on the User. Interceptors on role CRUD operations trigger this recalculation cascade, including a safety guard ensuring at least one user retains critical administrative permissions.

## Structure

```java
// RecalculatePermissions operation
Set<PermissionFlag> flags = new HashSet<>();
for (Role role : userDao.queryRoles(user).selectList()) {
    flags.addAll(roleDao.queryPermissions(role).selectList().stream()
        .map(Permission::getPermissionFlag).toList());
}
// Set individual boolean fields
user.setCanManageUsers(flags.contains(PermissionFlag.USERS));
user.setCanManageRoles(flags.contains(PermissionFlag.ROLES));
// ... 20+ more fields

// Dirty-check before persisting
Map<String, Object> before = new HashMap<>(user.toMap());
// ... set fields ...
if (!before.equals(user.toMap())) {
    userDao.update(user, UserMask.userMask());
}
```

## Examples

### RackInspect
22 permission flags (COMPANY_DATA, ROLES, USERS, FAULT_REGISTRIES, OFFERS, etc.). `RecalculatePermissionsCustomImplementation` iterates roles and sets boolean fields. `RoleSetAndRemoveAndDeleteInterceptor` recalculates ALL users on any role permission change. `UserRolesSetAndRemoveInterceptor` recalculates only the affected user. Safety guard prevents removing the last ROLES+USERS admin.

## Trade-offs

- Pros: Fast permission checks (single boolean field lookup), no join needed at query time, works with model-level access expressions
- Cons: O(N) recalculation for all users on role changes, 22+ boolean fields create wide entity, denormalization can drift if cascade is missed
- Alternative: Join-based permission check at query time, or external IdP (Keycloak) for role management

## Related

- [[interceptor-crud-lifecycle]]
- [[dirty-check-before-update]]


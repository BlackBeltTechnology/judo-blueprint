---
id: role-based-invitation-guard
title: Role-Based Invitation Permission Guard
description: A service-level authorization pattern that restricts which roles a user can assign when inviting others to an organization.
aliases: []
keywords: [role, based, invitation, permission, guard]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: auth
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
related: [actor-resolution-variable-resolver, typed-exception-error-handling, service-delegation-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

A service-level authorization pattern that restricts which roles a user can assign when inviting others to an organization. A static permission matrix maps each inviter role to the set of roles they are allowed to assign. The operation checks the current user's role against this matrix before creating the invitation, throwing a BusinessErrorException if unauthorized. This prevents privilege escalation through the invitation flow.

## Structure

```java
private static final Map<UserRole, Set<UserRole>> ALLOWED_INVITATION_ROLES = Map.of(
    UserRole.COMPANY_ADMIN, Set.of(UserRole.COMPANY_ADMIN, UserRole.COMPANY_READER),
    UserRole.PLATFORM_ADMIN, Set.of(UserRole.PLATFORM_ADMIN, UserRole.ASSOCIATION_LEADERSHIP),
    UserRole.ASSOCIATION_LEADERSHIP, Set.of(UserRole.ASSOCIATION_LEADERSHIP)
);

@Override
public void accept(Panel _this, InvitationInput input) throws BusinessErrorException {
    User currentUser = actorService.getCurrentUser();
    UserRole inviterRole = currentUser.getRole();
    UserRole requestedRole = input.getRole();

    Set<UserRole> allowed = ALLOWED_INVITATION_ROLES.getOrDefault(inviterRole, Set.of());
    if (!allowed.contains(requestedRole)) {
        throw ExceptionUtils.createBusinessErrorException(
            "FORBIDDEN_ROLE_INVITATION",
            "You are not authorized to invite users with this role");
    }

    // Proceed with invitation
    userService.inviteUser(input, organization);
    auditLogService.log(AuditActionType.INVITATION_SENT, ...);
}
```

## Examples

### mlszksz-platform
`InviteUserCustomImplementation` defines a static `ALLOWED_INVITATION_ROLES` map: COMPANY_ADMIN can invite COMPANY_ADMIN and COMPANY_READER; PLATFORM_ADMIN can invite PLATFORM_ADMIN and ASSOCIATION_LEADERSHIP; ASSOCIATION_LEADERSHIP can invite ASSOCIATION_LEADERSHIP only. Prevents privilege escalation (e.g., a COMPANY_ADMIN cannot create PLATFORM_ADMIN invitations). Validated in integration tests via `InviteUserRoleValidationTest`.

## Trade-offs

- Pros: Prevents privilege escalation, declarative permission matrix is easy to audit, centralized in the operation, tested via integration tests
- Cons: Hardcoded in Java (not configurable at runtime), permission matrix must be maintained when new roles are added, no model-level enforcement
- Alternative: Model-level access control expressions, database-driven permission matrix, or Keycloak role-based access policies

## Related

- [[actor-resolution-variable-resolver]]
- [[typed-exception-error-handling]]
- [[service-delegation-pattern]]


---
id: role-based-invitation-guard
title: Role-Based Invitation Permission Guard
description: "A static matrix inside a custom operation restricts which roles an inviter may assign, so the invitation flow cannot be used for privilege escalation."
aliases: [invitation role matrix, privilege escalation guard]
keywords: [role, invitation, permission matrix, privilege escalation, custom operation, guard]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: auth
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
related: [actor-resolution-variable-resolver, typed-exception-error-handling, service-delegation-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An invitation operation lets a user create an invitation that carries a role for the invitee. Without a check, an inviter could hand out a role stronger than their own. A static matrix maps each inviter role to the set of roles that inviter may assign, and the operation checks it before it creates anything.

## Practice

### Platform base

- An invitation is a custom operation, so its logic is your own `<Op>CustomImplementation` OSGi component ([custom operations](../../agent-docs/backend/custom-operations.md)).
- Interceptors fire only for built-in behaviour operations. Permission checks for custom operations must be written inside the implementation, and hiding a button in the UI does not protect the operation ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- A refusal is a business error. The operation can throw a fault it declares in the model; the generated `<Fault>Exception` is checked, and the operation must declare the fault or Maven fails with a `throws` clause error ([modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)). On the wire it is HTTP 422 with the fault FQN in `X-Fault`.
- Names such as `BusinessErrorException` exist only if the project models a fault called `BusinessError`; they are not platform classes.

### Project practice: the role matrix

This layer is project practice (mlszksz-platform), not a platform feature:

- Keep one constant map from inviter role to the allowed set of invited roles. An unknown inviter role gets the empty set, so the default is deny.
- Resolve the caller's role from the current user (the project's actor service, see [[actor-resolution-variable-resolver]]) and compare it with the role on the input, before any side effect.
- Throw a stable error code such as `FORBIDDEN_ROLE_INVITATION` and only then call the service that creates the invitation.
- Every role list is a domain decision. Adding a role means touching the matrix and its test.

```java
// Example project code: actorService, userService, auditLogService and ExceptionUtils are project classes
private static final Map<UserRole, Set<UserRole>> ALLOWED_INVITATION_ROLES = Map.of(
    UserRole.COMPANY_ADMIN, Set.of(UserRole.COMPANY_ADMIN, UserRole.COMPANY_READER),
    UserRole.PLATFORM_ADMIN, Set.of(UserRole.PLATFORM_ADMIN, UserRole.ASSOCIATION_LEADERSHIP),
    UserRole.ASSOCIATION_LEADERSHIP, Set.of(UserRole.ASSOCIATION_LEADERSHIP)
);

@Override
public void accept(Panel _this, InvitationInput input) throws BusinessErrorException {
    UserRole inviterRole = actorService.getCurrentUser().getRole();
    Set<UserRole> allowed = ALLOWED_INVITATION_ROLES.getOrDefault(inviterRole, Set.of());
    if (!allowed.contains(input.getRole())) {
        // BusinessErrorException is the project's own modeled fault
        throw ExceptionUtils.createBusinessErrorException(
            "FORBIDDEN_ROLE_INVITATION",
            "You are not authorized to invite users with this role");
    }
    userService.inviteUser(input, organization);
    auditLogService.log(AuditActionType.INVITATION_SENT, ...);
}
```

## Rationale

- The matrix is declarative and easy to audit, and the check sits next to the only code path that creates invitations.
- Interceptors cannot do this job here, because they never fire for custom operations.
- Deny by default means a new role is not invitable until someone adds it on purpose.

## Example

In mlszksz-platform the invite operation defines the map: a company admin may invite company admins and company readers, a platform admin may invite platform admins and association leadership, association leadership may invite association leadership only. A company admin therefore cannot create a platform admin invitation. An integration test, `InviteUserRoleValidationTest`, covers the matrix.

## When to avoid

- The rules change at runtime or per tenant: keep the matrix in data, not in a Java constant.
- Other custom operations also hand out roles: share the check in one service, otherwise the matrix is bypassed through them.
- A permission that is really about what an actor can see or reach: model it in the actor's transfer objects and accesses instead.

## Related

- [[actor-resolution-variable-resolver]] — how the project finds the current user and role
- [[typed-exception-error-handling]] — the modeled fault used for the refusal
- [[service-delegation-pattern]] — the services the operation calls after the check

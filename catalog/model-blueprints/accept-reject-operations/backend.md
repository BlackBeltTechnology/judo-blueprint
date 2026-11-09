## Overview

The accept/reject operations are implemented as thin custom operation classes that delegate to shared service layers (RegistrationService, InvitationService), each logging an audit event after the state transition completes.

## Implementation Pattern

Each accept/reject operation is a separate `@Component` class implementing the generated operation interface (e.g., `Accept`, `Reject`). The class injects a domain-specific service (`RegistrationService` or `InvitationService`) via `@Reference` and an `AuditLogService` for cross-cutting audit logging. The service layer performs status validation (must be VERIFIED), authorization checks (organization-scoped access for CompanyAdmin), entity creation (User + Keycloak account on accept), email dispatch (magic link on accept), and status update (APPROVED or REJECTED). Reject operations validate the same preconditions but only update the status. Both throw `BusinessErrorException` for invalid state transitions.

## Examples

### mlszksz-platform
- Key files: `custom/.../registrationrequest/AcceptCustomImplementation.java`, `custom/.../registrationrequest/RejectCustomImplementation.java`, `custom/.../userinvitationrequestto/AcceptCustomImplementation.java`, `custom/.../userinvitationrequestto/RejectCustomImplementation.java`
- Pattern: Two parallel accept/reject pairs -- one for RegistrationRequest (delegating to `registrationService.approve()`/`reject()`) and one for UserInvitationRequestTO (delegating to `invitationService.accept()`/`reject()`)
- Service layer: `RegistrationServiceImpl` validates VERIFIED status, checks duplicate org names, creates Organization + User + Keycloak user, sends approval email with magic link; `InvitationServiceImpl` validates VERIFIED status, checks organization access (PlatformAdmin can manage all, CompanyAdmin only own org), creates User + Keycloak user
- Audit: Every accept/reject logs via `auditLogService.log()` with action type (REGISTRATION_APPROVED, INVITATION_ACCEPTED, etc.) and contextual details (email, organizationName)
- Notable: Accept operations create Keycloak users and generate magic links for one-click login; reject is a status-only update

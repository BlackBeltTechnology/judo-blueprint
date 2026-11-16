## Overview

The organization is managed through custom operations that call a project service. The service holds the rules: unique names, status transitions, and address composition. The generated built-in operations (create, update, delete, list) still run, but interceptors do not run around custom operations, so every rule that matters for a custom operation sits in the operation or its service.

## Implementation Pattern

- **Service (example project code, not platform API):** a service class with the operations as methods. It receives DAOs and a user service through dependency injection.
- **Creation:** a custom create operation checks that the name and the user email are unique, creates the organization with status ACTIVE, and creates the first administrator user through the user service.
- **Profile update:** a custom operation updates the profile fields from a transfer object and replaces the capability set (remove all, then add the new ones). Renaming is limited to platform administrators.
- **Address update:** a custom operation creates or updates the composed address, checks that postal code and city match the reference data, and recomputes the full address text in one shared helper.
- **Status transitions:** suspend requires ACTIVE and rejects the administrator organization; reactivate requires SUSPENDED. Each transition is a custom operation, because a plain update would let any status be written; the transition rules are project practice, kept in the operation (interceptors would not see custom operations).
- **Faults:** a business rule violation is a modeled fault in the operation signature (HTTP 422). Field validation is reported as a validation exception (HTTP 400). Project error helpers are not platform API.
- **Audit:** an interceptor does not see custom operations, so each status change writes its own audit row (see [[audit-log-entity]]).

## Examples

### Example (project code, not platform API)
- Pattern: the service handles creation with user provisioning, address composition and status rules; each custom operation is a thin wrapper over one service method.
- Notable: creating an organization is a compound action (organization, first user, identity-provider account). Address text uses a shared helper so registration and update produce the same format.

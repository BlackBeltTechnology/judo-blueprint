## Overview

The AuditLog entity is managed entirely through a centralized `AuditLogService` OSGi service. Every custom operation in the platform calls `auditLogService.log(...)` after performing its action, creating an immutable audit trail. The service auto-resolves the current user and organization from the JUDO security context. An `exportAuditLog` custom operation generates a CSV file from audit entries using `FileStoreService`.

## Implementation Pattern

- A shared `AuditLogService` interface with two methods: `log()` (auto-resolves user context via `VariableResolver`) and `logSystem()` (no user context, for automated actions)
- The implementation (`AuditLogServiceImpl`) is an OSGi `@Component` that uses `AuditLogDao` to create entries, `VariableResolver` to resolve the current user's email, and `UserDao` to look up the user's organization name for denormalization
- Every custom operation class injects `@Reference AuditLogService` and calls `auditLogService.log(AuditActionType.XXX, entityType, entityId, detailsMap)` as the last step
- Details are serialized to JSON via a `JsonUtils` utility
- The export operation queries `AuditLogDao` with optional date filtering, builds CSV with UTF-8 BOM, and stores via `FileStoreService`
- All audit log methods are exception-safe: failures are logged but never propagated to the caller

## Examples

### mlszksz-platform
- Key files: `common/services/AuditLogService.java`, `common/services/impl/AuditLogServiceImpl.java`, `custom/.../admindashboard/ExportAuditLogCustomImplementation.java`
- Pattern: Centralized service with `@Reference AuditLogDao`, `@Reference VariableResolver`, `@Reference UserDao`; auto-resolves user email from JUDO `ACTOR` context for denormalized `userName` and `organizationName` fields
- Notable: Export operation uses `FileStoreService` to persist CSV files; 32 `AuditActionType` enum members cover every domain event (USER_LOGIN, POST_PUBLISHED, ORGANIZATION_CREATED, etc.)
- Every custom operation (59 total) injects `AuditLogService` and logs its action with structured detail maps

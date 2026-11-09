## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::AuditLog`
  - Attributes: timestamp (req), actionType (req), entityType (req), entityId, details, userName, organizationName
  - Relations: user (0..1 ASSOCIATION to User)
  - Non-CRUD: createable=false, updateable=false, deleteable=false
- **Enum**: `MLSZKSZPlatform::types::AuditActionType` with 32 members covering USER_LOGIN, USER_CREATED, ORGANIZATION_CREATED, POST_PUBLISHED, ANNOUNCEMENT_DELETED, etc.
- **Transfer Object**: `MLSZKSZPlatform::services::admin::AuditLog` (mapped, read-only view for admin dashboard)
- Admin dashboard provides `exportAuditLog` operation for CSV export

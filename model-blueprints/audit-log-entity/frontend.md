## Overview

The audit log entity has extensive React frontend customization, including a custom "What" detail component with color-coded action types and parsed JSON details, plus a CSV export button added via container actions hook.

## Implementation Pattern

- **Custom visual element**: A Pandino-registered component replaces the default "What" section on the AuditLog detail view. It renders color-coded `Chip` components for each `AuditActionType` (user actions are blue, organization actions are purple, post actions are green, etc.), parses JSON details into labeled key-value pairs, and provides a copyable entity ID.
- **Container actions hook**: A separate hook adds an "Export CSV" toolbar button to the audit log table on the AdminDashboard. The button opens a `Dialog` with a `DatePicker` for selecting the export start date, then calls `exportAuditLog` and downloads the result as a file attachment.
- **i18n integration**: Custom translation keys for audit log detail labels (`custom.auditLog.detail.*`) and action type enum translations (`enumerations.AuditActionType.*`).

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/custom-implementations/registerServicesAdminAuditLogAuditLog_View_EditCustomImplementations.tsx`, `custom/hooks/custom-implementations/registerServicesAdminAdminDashboardAdminDashboard_View_EditCustomImplementations.tsx`
- Pattern: The AuditLog "What" component uses `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` to replace the generated form section. The CSV export is added via `auditLogAdditionalToolbarButtons` returned from a container actions hook, rendering an `ExportAuditLogButton` component with date picker dialog.
- Notable: Action type colors are mapped in a `Record<string, string>` covering all 32 `AuditActionType` members. JSON details are parsed with fallback to raw text display.

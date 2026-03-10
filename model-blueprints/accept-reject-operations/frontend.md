## Overview

The accept/reject operations pattern manifests in the React frontend through custom page action hooks that pre-filter approval tables to show only actionable items (e.g., VERIFIED status) and through dialog hooks that handle rejection reason input forms.

## Implementation Pattern

- **Table filtering hooks**: Page-level action hooks override `refreshAction` or `registrationRequestRefreshAction` to inject default filter criteria (e.g., `status = VERIFIED`) so admin tables only show items ready for approval.
- **Pandino registration**: Hooks are registered via `context.registerService` using the page actions hook interface key (e.g., `SERVICES_ADMIN_ADMIN_DASHBOARD_REGISTRATION_REQUEST_RELATION_TABLE_PAGE_ACTIONS_HOOK_INTERFACE_KEY`).
- **Two-hook pattern**: Both the embedded table (AccessViewPage hook) and the standalone table page (RelationTablePage hook) need the same filter to maintain consistent behavior.
- **Generated operation buttons**: The accept/reject buttons themselves use the generated UI with `enabledBy` guard attributes controlling visibility; no custom button rendering is needed.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/pages/registerServicesMLSZKSZAdminDashboardAccessViewPageActionsHook.ts`, `custom/hooks/pages/registerServicesAdminAdminDashboardRegistrationRequestRelationTablePageActionsHook.ts`
- Pattern: Both hooks override the refresh action to inject `status = VERIFIED` filter using `EnumerationOperation.equals`, ensuring admins only see registration requests ready for accept/reject decisions.
- Notable: The filtering is applied at two levels -- the embedded AdminDashboard table and the standalone RegistrationRequest table page -- using the same approach but different service implementations.

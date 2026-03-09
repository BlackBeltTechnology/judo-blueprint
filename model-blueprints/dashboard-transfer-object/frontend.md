## Overview

The dashboard transfer object has significant React frontend customization, including a custom inline statistics dashboard with KPI cards and sortable organization table, plus a custom CSV export button for audit logs.

## Implementation Pattern

- **Custom statistics component**: A Pandino-registered `CUSTOM_VISUAL_ELEMENT` replaces the generated statistics form with a visual dashboard. The `InlineStatisticsDashboard` wrapper auto-fetches statistics data via `getStatistics()` with a comprehensive mask including `organizationStatistics`, then renders `StatisticsDashboardView` with KPI cards, pending actions summary, content breakdown, user visibility metrics, and a sortable organization statistics table.
- **Statistics page mask override**: A page actions hook overrides `getMask()` to include the `organizationStatistics` nested relation, which the default generated mask would omit.
- **Container actions hook**: Adds custom toolbar buttons (e.g., audit log CSV export) to the AdminDashboard via `auditLogAdditionalToolbarButtons`.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/custom_views/InlineStatisticsDashboard.tsx`, `custom/custom_views/StatisticsDashboardView.tsx`, `custom/hooks/custom-implementations/registerServicesAdminAdminDashboardAdminDashboard_View_EditCustomImplementations.tsx`, `custom/hooks/pages/registerServicesAdminAdminDashboardStatisticsRelationViewPageActionsHook.ts`
- Pattern: The statistics component is registered as a custom visual element on the AdminDashboard. It fetches data independently and renders a dashboard with MUI `Card` KPI widgets and a sortable `Table` for per-organization statistics. The generated form for statistics is also overridden at the container level (`ServicesAdminStatisticsStatistics_View_Edit.tsx` in `.generator-ignore`).
- Notable: The statistics mask includes 16 count attributes and a nested `organizationStatistics` relation with 5 per-org metrics, requiring both inline and page-level mask overrides.

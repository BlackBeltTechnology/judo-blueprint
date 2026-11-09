## Overview

A custom admin statistics dashboard that replaces generated form layouts with KPI cards, content breakdowns, and a sortable organization table. Registered via Pandino custom visual element hooks. Framework: React.

## Implementation Pattern

The dashboard is implemented through two components registered in `application-customizer.tsx`:

- **StatisticsDashboardView** (`custom/custom_views/StatisticsDashboardView.tsx`) -- Pure presentation component that renders:
  - KPI Cards (Grid row): Total Users, Active Users (30d), Active Organizations, Total Content -- using MUI Card with icon, value, and label
  - Pending Actions: Pending Organization Requests and Pending User Invitations -- highlighted with warning color when non-zero
  - Content Breakdown: News, Offers, Requests, Announcements -- each showing all-time total and 30-day recent count
  - User Visibility: Hidden vs Visible users with percentage
  - Organization Statistics Table: Sortable MUI Table with columns (Organization, Total Users, Active Users, Hidden, Visible). Client-side sorting via React state.
- **InlineStatisticsDashboard** (`custom/custom_views/InlineStatisticsDashboard.tsx`) -- Wrapper that auto-fetches statistics data via `MLSZKSZServiceForAdminDashboardImpl.getStatistics()` and renders `StatisticsDashboardView` inline in the AdminDashboard's analytics tab. Uses a detailed `_mask` that includes `organizationStatistics{...}`.
- **Registration**: `registerServicesAdminAdminDashboardAdminDashboard_View_EditStatisticsComponentCustomImplementation(context)` replaces the default statistics visual element. `registerServicesAdminAdminDashboardStatisticsRelationViewPageActionsHook(context)` overrides the mask to include `organizationStatistics`.
- **CSS override**: `src/theme/index.css` contains `[data-name="analitics"] { box-shadow: none !important; background: transparent !important; }` to remove the generated Card frame from the analytics section.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/custom_views/StatisticsDashboardView.tsx`, `custom/custom_views/InlineStatisticsDashboard.tsx`, `custom/hooks/custom-implementations/registerServicesAdminAdminDashboardAdminDashboard_View_EditCustomImplementations.tsx`, `src/theme/index.css`
- Pattern: Custom visual element replaces generated statistics component; InlineStatisticsDashboard fetches data independently for tab-embedded display
- Notable: CSS hack removes generated card frame via `[data-name="analitics"]` selector; client-side sortable table for organization breakdown

## Overview

The multi-actor role-based projections pattern manifests extensively in the React frontend through role-aware navigation, custom view components per service package, and access guard hooks that control which dashboard and content views are available to each user role.

## Implementation Pattern

- **Role-aware feed navigation**: Page action hooks use `usePrincipal()` to check the current user's role and conditionally show features (e.g., the "Request Post" FAB is only shown for COMPANY_ADMIN and COMPANY_READER roles).
- **Per-package custom views**: Each service sub-package (admin, companyadmin, companyreader, feed) has dedicated custom view components. The admin package gets `InlineStatisticsDashboard` and CSV export; the companyadmin package gets content management dialog hooks; the companyreader package gets `ProfilePanelView`; the feed package gets `FeedContainer` and `DiscoveryContainer`.
- **Access-level hooks**: Page actions hooks are registered for different access points: `AdminDashboard/AccessViewPage`, `FeedDashboard/AccessViewPage`, `NotificationsDashboard/AccessViewPage`, each customizing mask and behavior for the corresponding role context.
- **Two frontend applications**: The project has two separate React apps -- the main app (`mlszkszplatform__services__mlszksz`) serving authenticated users across all roles, and a registration app (`mlszkszplatform__services__registration__registration_point`) serving the public registration flow for the RegistrationPoint actor.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/application-customizer.tsx`, `custom/hooks/pages/registerServicesMLSZKSZFeedDashboardAccessViewPageActionsHook.ts`, `custom/hooks/pages/registerServicesMLSZKSZAdminDashboardAccessViewPageActionsHook.ts`, `custom/hooks/custom-implementations/registerServicesCompanyreaderProfilePanelProfilePanel_View_EditCustomImplementations.tsx`
- Pattern: The `application-customizer.tsx` registers over 25 Pandino hooks covering admin (statistics, audit log, config), companyadmin (content editing, user invitation, address update), companyreader (profile panel), and feed (feed container, discovery, notifications) -- each tailored to the role's service package.
- Notable: Role routing happens at the application layer based on UserRole enum rather than separate actor applications. The single MLSZKSZ actor serves all roles, with frontend `usePrincipal()` and access guard attributes controlling what each role can see and do.

## Overview

The organization appears in the frontend through two custom views: a full organization profile page, and a card in the discovery list. Both show the logo, contact details, capabilities and membership information.

## Implementation Pattern

- **Profile view:** a custom view registered for the organization's reader container replaces the generated form with a styled profile. It shows the logo, contact actions (mail and phone links), capability chips, membership dates and the full address.
- **Discovery card:** the discovery panel shows organization cards (see [[organization-discovery-search-component]]). The card reuses the profile view's logo and contact parts.
- **Portal injection:** a custom view mounts in a portal and hides the generated view page container. A mutation observer finds that container when it renders.
- **Page mask:** a page actions hook extends the query mask of the discovery detail page with the capability names, so the chips can render.
- **Hook keys:** registration keys are generated per page or container. Copy them from the generated customizer of your own project.

## Examples

### mlszksz-platform (example project code, not platform API)
- Framework: React
- Key files: `custom/custom_views/OrganizationView.tsx`, `custom/hooks/containers/registerServicesCompanyReaderOrganizationContainerHook.tsx`, `custom/hooks/containers/registerServicesFeedOrganizationSearchContainerHook.tsx`, `custom/hooks/pages/registerServicesFeedDiscoveryPanelOrganizationSearchRelationViewPageActionsHook.tsx`
- Pattern: a `useLogoUrl` hook downloads the logo through the access service and creates a blob URL; contact actions render `mailto:` and `tel:` links.
- Notable: the same view serves the user's own organization profile and the public discovery detail, registered through two container hooks.

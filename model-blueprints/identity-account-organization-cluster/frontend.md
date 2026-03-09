## Overview

The identity-account-organization-cluster blueprint has substantial React frontend customization in the account actor application. The key frontend implementation is a custom organization selector in the AppBar that allows users to switch between organizations, combined with an axios interceptor that passes the selected organization as a request header, a navigation interceptor that preserves the organization query parameter across page transitions, a custom landing page with principal-guarded action tiles, and a fully overridden PartnerDashboard page.

## Implementation Pattern

- **Organization selector AppBar component**: A custom `AppBarExtraComponents` hook registers a visual element component that renders an organization dropdown in the AppBar. It fetches the user's organizations via `AccountActorServiceForOrganizationsImpl.list()`, displays them in a MUI Menu, and updates the `organization` URL search parameter on selection. When the current organization is not found in the list, it auto-selects the first available organization and reloads.
- **Axios interceptor for organization context**: A custom axios request interceptor extracts the `organization` query parameter from `window.location` and injects it as `X-Judo-RequestParameters` header, enabling the backend to scope all API responses to the selected organization.
- **Navigation interceptor**: A `NavigationInterceptorHook` preserves search parameters (including the organization) across internal navigation so the selected organization persists through page transitions.
- **Custom PartnerDashboard page**: The generated PartnerDashboard AccessViewPage is overridden via `.generator-ignore` with a custom tile-based dashboard. The dashboard uses `principal.isOrganizationSelected` to conditionally show action tiles (Invite Administrator, Invite User, Create Application) alongside the always-visible Create Organization tile. Each tile opens the corresponding dialog form.
- **Custom landing/guest page**: A `LandingPage` component registered with `GUEST_PAGE_INTERFACE_KEY` provides a branded login/registration page with a background image and OIDC sign-in redirect.
- **Principal refresh on context change**: The organization selector calls `refreshPrincipal()` after changing organizations to update the principal's guard flags (e.g., `isOrganizationSelected`), which control conditional UI visibility.

## Examples

### ubives
- Framework: React
- Key files: `ubives__services__account_actor/src/custom/hooks/AppBar/AppBarExtraComponents.tsx`, `ubives__services__account_actor/src/custom/hooks/Navigation/CustomAxiosInterceptor.ts`, `ubives__services__account_actor/src/custom/hooks/Navigation/CustomNavigationInterceptor.ts`, `ubives__services__account_actor/src/custom/LandingPage.tsx`, `ubives__services__account_actor/src/pages/Services/AccountActor/PartnerDashboard/AccessViewPage/index.tsx`
- Pattern: The AppBar organization selector fetches DashboardOrganization TOs, renders a dropdown menu, and sets the `organization` search parameter. An axios interceptor passes this as `X-Judo-RequestParameters`. The PartnerDashboard is replaced with a custom tile-based dashboard that uses `principal.isOrganizationSelected` to conditionally show invite/create actions.
- Notable: The organization context flows entirely via URL query parameters and HTTP headers rather than being stored in session state, making the selected organization bookmarkable and shareable. The `refreshPrincipal()` call after organization change ensures the principal's derived guard flags update immediately.

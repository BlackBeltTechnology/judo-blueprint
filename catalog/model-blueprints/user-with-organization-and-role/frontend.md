## Overview

The user entity with organization and role manifests in the React frontend through a custom profile panel that replaces the generated form with instant-save notification preferences using Switch components, and through role-aware behavior across the application.

## Implementation Pattern

- **Custom ProfilePanelView**: A Pandino-registered `CUSTOM_VISUAL_ELEMENT` replaces the generated ProfilePanel form with `ProfilePanelView`. This component displays profile information (name, email, organization link) as read-only fields, and notification preferences (notifyOffers, notifyRequests, notifyAnnouncements, notifyNews) as `Switch` components with debounced instant save -- no edit mode needed.
- **Role-aware UI**: The `usePrincipal()` hook is used across the application to check the user's role for conditional rendering (e.g., showing the "Request Post" FAB only for COMPANY_ADMIN/COMPANY_READER roles).
- **Organization navigation**: The profile panel includes a clickable organization link that navigates to the CompanyReaderOrganization detail page using `SingleRelationInput` component.
- **Passkey setup**: The profile panel includes a "Setup Passkey" button that initiates the `requestPasskeySetup` operation for passwordless authentication.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/custom_views/ProfilePanelView.tsx`, `custom/hooks/custom-implementations/registerServicesCompanyreaderProfilePanelProfilePanel_View_EditCustomImplementations.tsx`
- Pattern: The ProfilePanelView uses MUI `Switch` components for notification flags, `debounce` from MUI utils for text field changes, and calls the update service directly on change without requiring the user to enter edit mode. The `Section` component from shared custom views provides consistent section layout.
- Notable: The profile panel integrates with native Capacitor authentication by importing `storePkceParams` and `generateState` from the custom auth module for passkey setup.

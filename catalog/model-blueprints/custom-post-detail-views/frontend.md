## Overview

Custom view components that replace the default generated container layouts for post detail pages and related entity views with mobile-optimized, visually designed read-only layouts. Framework: React.

## Implementation Pattern

The platform's container hook does not replace a layout: a container's hook (`<Container>ContainerHook`, registered through the container's generated actions hook key) returns action handlers and validation props for the generated page ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)). To render a custom layout, the view must be a visual element that the UI model declares as a custom implementation widget. It is then registered as a component under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with the element's generated `component` key, from the generated scaffold of the container's custom implementations ([advanced patterns](../../agent-docs/frontend/advanced-patterns.md), Component Replacement Hook). The project may additionally register container hooks for the actions of the same pages. The views and helpers below are example project code:

- **PostViewLayout** (`custom/custom_views/shared/PostViewLayout.tsx`) -- Shared wrapper providing responsive padding, a MUI Paper card with type-colored left border (`4px solid {typeColor}`), and loading opacity transition. Used by all post views.
- **Section / MetaRow** -- Shared helper components for consistent section headers (uppercase, secondary color) and meta information rows (type chip, author, date separated by bullet dots).
- **NewsView** (`custom/custom_views/NewsView.tsx`) -- Displays title, type chip, author, published date, description (pre-wrap), optional featured image (downloaded via the project's `AccessServiceImpl.downloadFile` helper), organization card, and contact actions.
- **OfferView** (`custom/custom_views/OfferView.tsx`) -- Adds validity period, capabilities, description, interest button, organization card, and contact actions.
- **RequestView** (`custom/custom_views/RequestView.tsx`) -- Adds deadline, capabilities, description, interest button, organization card, and contact actions.
- **AnnouncementView** (`custom/custom_views/AnnouncementView.tsx`) -- Displays title, description, optional image, author, and published date.
- **OrganizationView** (`custom/custom_views/OrganizationView.tsx`) -- Displays organization details (name, address, logo, capabilities, contact info) for the discovery panel detail page.
- **ProfilePanelView** (`custom/custom_views/ProfilePanelView.tsx`) -- Custom profile page with instant-save debounced inputs and Switch components for notification preferences.
- **ContactActions** (`custom/custom_views/shared/ContactActions.tsx`) -- Email/phone action buttons that open `mailto:` / `tel:` links.
- **OrganizationCard** (`custom/custom_views/shared/OrganizationCard.tsx`) -- Compact organization info card with logo, name, city, used in post views.
- **InterestButton** (`custom/custom_views/shared/InterestButton.tsx`) -- Button for expressing interest in offers/requests.

**Registration** (project code): the project's registration functions in `custom/hooks/containers/`, e.g. `registerServicesFeedNewsContainerHook(context)`, receive the page's `data` and `actions` props and render the custom view. The exact registration kind must follow the generated scaffold; the platform docs describe the custom implementation element as the route for replacing a layout.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/custom_views/NewsView.tsx`, `custom/custom_views/OfferView.tsx`, `custom/custom_views/RequestView.tsx`, `custom/custom_views/AnnouncementView.tsx`, `custom/custom_views/OrganizationView.tsx`, `custom/custom_views/ProfilePanelView.tsx`, `custom/custom_views/shared/PostViewLayout.tsx`, `custom/hooks/containers/`
- Pattern: Registered project views replace generated layouts with type-specific mobile-optimized views sharing PostViewLayout wrapper
- Notable: Binary image download via AccessServiceImpl; ProfilePanelView uses instant-save with debounced inputs instead of edit/save cycle; post type color coding shared with feed cards via `getTypeColor` utility

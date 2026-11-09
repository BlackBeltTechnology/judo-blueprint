## Overview

Custom view components that replace the default generated container layouts for post detail pages and related entity views with mobile-optimized, visually designed read-only layouts. Registered as Pandino container hooks. Framework: React.

## Implementation Pattern

The pattern uses Pandino container hooks to replace the default generated container components for specific transfer object view pages:

- **PostViewLayout** (`custom/custom_views/shared/PostViewLayout.tsx`) -- Shared wrapper providing responsive padding, a MUI Paper card with type-colored left border (`4px solid {typeColor}`), and loading opacity transition. Used by all post views.
- **Section / MetaRow** -- Shared helper components for consistent section headers (uppercase, secondary color) and meta information rows (type chip, author, date separated by bullet dots).
- **NewsView** (`custom/custom_views/NewsView.tsx`) -- Displays title, type chip, author, published date, description (pre-wrap), optional featured image (downloaded via `AccessServiceImpl.downloadFile`), organization card, and contact actions.
- **OfferView** (`custom/custom_views/OfferView.tsx`) -- Adds validity period, capabilities, description, interest button, organization card, and contact actions.
- **RequestView** (`custom/custom_views/RequestView.tsx`) -- Adds deadline, capabilities, description, interest button, organization card, and contact actions.
- **AnnouncementView** (`custom/custom_views/AnnouncementView.tsx`) -- Displays title, description, optional image, author, and published date.
- **OrganizationView** (`custom/custom_views/OrganizationView.tsx`) -- Displays organization details (name, address, logo, capabilities, contact info) for the discovery panel detail page.
- **ProfilePanelView** (`custom/custom_views/ProfilePanelView.tsx`) -- Custom profile page with instant-save debounced inputs and Switch components for notification preferences.
- **ContactActions** (`custom/custom_views/shared/ContactActions.tsx`) -- Email/phone action buttons that open `mailto:` / `tel:` links.
- **OrganizationCard** (`custom/custom_views/shared/OrganizationCard.tsx`) -- Compact organization info card with logo, name, city, used in post views.
- **InterestButton** (`custom/custom_views/shared/InterestButton.tsx`) -- Button for expressing interest in offers/requests.

**Registration**: Each view is registered via a container hook in `custom/hooks/containers/`, e.g., `registerServicesFeedNewsContainerHook(context)`, `registerServicesFeedOfferContainerHook(context)`. The container hooks receive the page's `data` and `actions` props and render the custom view.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/custom_views/NewsView.tsx`, `custom/custom_views/OfferView.tsx`, `custom/custom_views/RequestView.tsx`, `custom/custom_views/AnnouncementView.tsx`, `custom/custom_views/OrganizationView.tsx`, `custom/custom_views/ProfilePanelView.tsx`, `custom/custom_views/shared/PostViewLayout.tsx`, `custom/hooks/containers/`
- Pattern: Container hooks replace generated layouts with type-specific mobile-optimized views sharing PostViewLayout wrapper
- Notable: Binary image download via AccessServiceImpl; ProfilePanelView uses instant-save with debounced inputs instead of edit/save cycle; post type color coding shared with feed cards via `getTypeColor` utility

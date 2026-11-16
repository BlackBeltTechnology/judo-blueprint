## Overview

Custom view components that replace the default generated container layouts for post detail pages and related entity views with mobile-optimized, visually designed read-only layouts. Framework: React.

## Implementation Pattern

The platform's container hook does not replace a layout: a container's hook (`<Container>ContainerHook`, registered through the container's generated actions hook key) returns action handlers and validation props for the generated page ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)). To render a custom layout, the view must be a visual element that the UI model declares as a custom implementation widget. It is then registered as a component under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with the element's generated `component` key, from the generated scaffold of the container's custom implementations ([advanced patterns](../../agent-docs/frontend/advanced-patterns.md), Component Replacement Hook). The project may additionally register container hooks for the actions of the same pages. The views and helpers below are reference implementation code:

- **PostViewLayout** -- Shared wrapper providing responsive padding, a MUI Paper card with type-colored left border (`4px solid {typeColor}`), and loading opacity transition. Used by all post views.
- **Section / MetaRow** -- Shared helper components for consistent section headers (uppercase, secondary color) and meta information rows (type chip, author, date separated by bullet dots).
- **NewsView** -- Displays title, type chip, author, published date, description (pre-wrap), optional featured image (downloaded via the application's `AccessServiceImpl.downloadFile` helper), organization card, and contact actions.
- **OfferView** -- Adds validity period, capabilities, description, interest button, organization card, and contact actions.
- **RequestView** -- Adds deadline, capabilities, description, interest button, organization card, and contact actions.
- **AnnouncementView** -- Displays title, description, optional image, author, and published date.
- **OrganizationView** -- Displays organization details (name, address, logo, capabilities, contact info) for the discovery panel detail page.
- **ProfilePanelView** -- Custom profile page with instant-save debounced inputs and Switch components for notification preferences.
- **ContactActions** -- Email/phone action buttons that open `mailto:` / `tel:` links.
- **OrganizationCard** -- Compact organization info card with logo, name, city, used in post views.
- **InterestButton** -- Button for expressing interest in offers/requests.

**Registration** (application code): the application's registration functions in its container hooks folder, e.g. `registerServicesFeedNewsContainerHook(context)`, receive the page's `data` and `actions` props and render the custom view. The exact registration kind must follow the generated scaffold; the platform docs describe the custom implementation element as the route for replacing a layout.

## Examples

### Variant seen in practice
- Framework: React
- Pattern: Registered project views replace generated layouts with type-specific mobile-optimized views sharing PostViewLayout wrapper
- Notable: Binary image download via AccessServiceImpl; ProfilePanelView uses instant-save with debounced inputs instead of edit/save cycle; post type color coding shared with feed cards via `getTypeColor` utility

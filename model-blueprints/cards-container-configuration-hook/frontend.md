## Overview

A Pandino hook pattern that configures the `CardsContainer` component to render relation/table data as custom MUI Card components instead of the default data grid rows. The hook replaces the `CardElement` while preserving the container's built-in pagination, filtering, and data fetching. Framework: React.

## Implementation Pattern

- **Hook type**: `*CardsContainerConfigHook` -- each table/relation component generates its own typed hook interface (e.g., `ServicesUserReservationPanelUserReservationPanel_View_EditUserReservationsComponentCardsContainerConfigHook`)
- **Registration key**: `*_CARDS_CONTAINER_CONFIG_HOOK_INTERFACE_KEY` -- imported from the component's `customization` module (e.g., `~/containers/Services/UserReservationPanel/.../customization`)
- **Registration**: A `register*ComponentCardsContainerConfig(context)` function registered in `application-customizer.tsx`
- **Hook return shape**: Object with optional properties:
  - `CardElement` (required in practice) -- a React FC receiving `CardProps<TStored, TRowActionDefinitions>` with `{ row, columns, onRowClick, actions }`
  - `ToolbarElement` (optional) -- custom toolbar FC for filters/search
  - `ActionbarElement` (optional) -- custom action bar FC
  - `layout` (optional) -- `'horizontal'` or default vertical
  - `showPagination` (optional) -- boolean
- **Card component pattern**: The custom `CardElement` delegates to a separate reusable card component (e.g., `UserActiveReservationsCard`), wrapping it in a `<Grid item>` with responsive breakpoints
- **Grid wrapping**: Every custom card MUST be wrapped in `<Grid item xs={12} sm={12} md={6} lg={4} xl={4}>` (or similar) to ensure proper responsive layout across devices
- **Card content**: Typically uses MUI `Card`, `CardContent`, `CardActions`, `List`/`ListItem` with `MdiIcon`, `Typography`, and optionally `Timeline` from `@mui/lab` for temporal data
- **Actions**: Card action buttons call `actions.*Action?.(row)` with optional `openConfirmDialog` for destructive operations
- **Hooks inside cards**: Custom card components can use `useTranslation`, `useTheme`, `useL10N`, `useConfirmDialog`, and `useViewData`
- **Multiple instances**: A single project may have multiple `CardsContainerConfigHook` registrations for different views/relations, each with its own custom card component

## Examples

### park-here
- Framework: React
- Key files: `custom/hooks/components/cards/registerServicesUserReservationPanelUserReservationPanel_View_EditUserReservationsComponentConfigurationHook.tsx`, `custom/hooks/components/cards/registerServicesHolidayPanelHolidayPanel_View_EditHolidaysComponentConfigurationHook.tsx`, `custom/hooks/components/cards/registerServicesUserReservationPanelUserReservationPanel_View_EditPreviousReservationComponentConfigurationHook.tsx`, `custom/hooks/components/UserActiveReservationsCard.tsx`, `custom/hooks/components/UserPreviousReservationsCard.tsx`, `custom/hooks/components/HolidayCard.tsx`
- Pattern: Three separate `CardsContainerConfigHook` registrations replace table views with card layouts for active reservations (timeline-based cards with start/end time visualization), previous reservations (horizontal list-based summary cards), and holidays (cards with decorative image and colored bottom bar)
- Notable: `UserActiveReservationsCard` uses `@mui/lab` Timeline component for time range visualization; cards conditionally render action buttons (delete, cancel, modify) based on row state flags (`isNotDeletable`, `isNotCancelable`); `HolidayCard` includes an `ImageDisplay` component with fallback SVG; responsive Grid breakpoints vary per card type (4-column grid for active, full-width for previous)

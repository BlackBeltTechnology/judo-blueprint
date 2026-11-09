## Overview

A custom admin statistics visual replaces the generated statistics panel with KPI cards, pending-action counters, a content breakdown and a sortable organization table. The visual is registered as a custom implementation of the generated component. Framework in the reference project: React with MUI.

## Presentation component

### Pure presentation of the statistics

The presentation component takes the statistics object as props and renders:

- **KPI cards** in a grid row: total users, active users (30 days), active organizations and total content. Each card has an icon, a value and a label.
- **Pending actions**: counters for pending organization requests and pending user invitations, shown with a warning colour when the value is non-zero.
- **Content breakdown**: one row per content type with the all-time total and the 30-day count.
- **User visibility**: hidden against visible users, with percentages.
- **Organization table**: a sortable table (organization, total users, active users, hidden, visible). Sorting is client-side, held in component state.

Keep this component free of data fetching so that it can be reused by every host.

## Hosts

### Standalone page and dashboard tab

Two hosts render the same presentation:

- The standalone view page passes the data it already has from the page context.
- An inline host fetches the statistics itself, so it works in a dashboard tab that has no page data. In the reference project the fetch is done by a project service class (`MLSZKSZServiceForAdminDashboardImpl.getStatistics()`), which is example project code, not platform API. Its data mask must include the nested organization statistics.

## Registration

### Custom implementation hooks

The custom visual is attached through the generated customization hooks. The hook key for the statistics component is generated per page and per container; take the exact name from the generated hook file of the page, do not copy it from another project. Two registrations are involved:

- a custom implementation that replaces the default statistics visual element;
- a data-mask hook for the relation view page that adds the nested organization statistics to the fetch.

## Styling

### Removing the generated card frame

The generated analytics section is wrapped in a card. A style override on that section's data-name attribute removes the box shadow and the background so the custom visual sits on the page directly. Select on the generated attribute, not on a class name, because class names change between generator runs.

## Examples

### Reference project

- Framework: React with MUI.
- Key files: a presentation component, an inline host, the generated customization hook file of the admin dashboard and the theme stylesheet.
- Pattern: the custom visual replaces the generated statistics component; the inline host fetches its data separately for the tab.
- Notable: the card frame is removed with a selector on the generated section attribute; the organization table is sorted on the client.

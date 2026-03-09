## Overview

The capability lookup entity manifests in the React frontend through autocomplete-based capability filtering in the feed and discovery components, and through dialog action hooks that autofill capability data in update forms.

## Implementation Pattern

- **Autocomplete filtering**: A custom `useCapabilitiesAutocomplete` hook provides type-ahead capability selection for feed and discovery filters. The hook queries the capabilities list from the FeedPanel and populates an MUI `Autocomplete` component.
- **Update dialog hooks**: Dialog-level action hooks for the Capability update form use `postGetTemplateAction` to pre-fill the form with existing capability data (name, description) when editing.
- **Feed integration**: Capabilities are displayed as `Chip` components on `FeedEntryCard` and `DiscoveryOrganizationCard`, parsed from a semicolon-delimited string (`entry.capabilities?.split(';')`).

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/feedComponent/hooks/useCapabilitiesAutocomplete.ts`, `custom/hooks/dialogs/registerServicesAdminCapabilityCapability_View_EditUpdateCapabilityInputFormActionsHook.ts`, `custom/hooks/dialogs/registerServicesAdminAdminDashboardAdminDashboard_View_EditCapabilitiesUpdateCapabilityInputFormActionsHook.ts`
- Pattern: The capabilities autocomplete hook is shared between the feed and discovery filter components. The admin update dialog hooks pre-populate the form with existing name and description from the current capability.
- Notable: Capabilities appear in three distinct UI contexts: feed entry cards (as chips), discovery organization cards (as chips), and feed filter bar (as autocomplete).

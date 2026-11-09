## Overview

The platform configuration singleton manifests in the React frontend through a dialog action hook that pre-fills the configuration update form with current values from the Configuration entity.

## Implementation Pattern

- **Dialog postGetTemplate hook**: A Pandino-registered dialog actions hook provides a `postGetTemplateAction` callback that fires after the update form template is loaded. It fetches the current configuration values via `configService.refresh()` with a mask covering all editable fields, then calls `storeDiff` for each field to populate the form.
- **Field-by-field autofill**: The hook iterates over each configuration field (senderEmail, baseUrl, platformName, invitationExpiryDays, verificationExpiryMinutes, and all email templates) and calls `storeDiff` individually, only setting values that exist.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesAdminAdminConfigurationTOAdminConfigurationTO_View_EditUpdateConfigurationInputFormActionsHook.ts`
- Pattern: The hook fetches the existing configuration using `ServicesadminAdminConfigurationTOServiceImpl.refresh()` with a mask covering 9 fields, then pre-fills the ConfigurationInput form via `storeDiff`. This avoids the user seeing an empty form when editing existing configuration.
- Notable: This is a common JUDO pattern for edit-via-input-TO operations where the input TO is different from the mapped TO, requiring explicit data loading into the form.

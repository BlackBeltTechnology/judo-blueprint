## Overview

The publish/delete/edit operations pattern manifests in the React frontend through dialog action hooks that pre-fill edit forms with existing content data when editing published or draft content items.

## Implementation Pattern

- **Dialog postGetTemplate hooks**: Each content type's edit operation dialog (editNews, editOffer, editRequest, editAnnouncement) has a Pandino-registered dialog actions hook that provides `postGetTemplateAction`. This callback fetches the current content data from the server and populates the edit form via `storeDiff` calls for each field.
- **Content-type-specific autofill**: Each hook fetches the relevant fields for its content type -- News gets title/description/image; Offer gets title/description/price/validFrom/validUntil/capabilities; Request gets title/description/deadline/capabilities; Announcement gets title/description/isSensitive/isStrategic.
- **Generated operation buttons**: The publish, delete, and moderationDelete buttons use the generated UI with guard attributes (`isNotPublisheable`, `isNotDeletable`, `isNotExpireble`) controlling visibility. No custom button rendering is needed for these.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesCompanyadminOrganizationAdminPanelOrganizationAdminPanel_View_EditNewsEditNewsInputFormActionsHook.ts`, `custom/hooks/dialogs/registerServicesCompanyadminOrganizationAdminPanelOrganizationAdminPanel_View_EditOffersEditOfferInputFormActionsHook.ts`, `custom/hooks/dialogs/registerServicesCompanyadminOrganizationAdminPanelOrganizationAdminPanel_View_EditRequestsEditRequestInputFormActionsHook.ts`, `custom/hooks/dialogs/registerServicesAdminAdminDashboardAdminDashboard_View_EditAnnouncementsEditAnnouncementInputFormActionsHook.ts`
- Pattern: Each dialog hook fetches the current content using the parent service (e.g., `OrganizationAdminPanelService`) with a content-type-specific mask, then calls `storeDiff` for each field. This is needed because the edit operation uses an unmapped Input TO that is separate from the content's mapped TO.
- Notable: The edit pattern is consistent across all four content types (news, offer, request, announcement) but lives in different service packages (companyadmin for the first three, admin for announcements).

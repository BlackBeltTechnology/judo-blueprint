## Examples

### mlszksz-platform
Content transfer objects in the `companyadmin` service package all follow this pattern:
- **News**: publish, delete, editNews, moderationDelete; guards: isNotPublisheable, isNotDeletable
- **Offer**: publish, delete, editOffer, expired, moderationDelete; guards: isNotPublisheable, isNotDeletable, isNotExpireble
- **Request**: publish, delete, editRequest, expired, moderationDelete; guards: isNotPublisheable, isNotDeletable, isNotExpireble
- **Announcement** (admin service): publish, delete, editAnnouncement; guards: isEditable, isDeletable, isPublishable
- All operations are INSTANCE type, non-custom (generated from model behavior)

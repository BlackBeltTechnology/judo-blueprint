## Examples

### mlszksz-platform
- **PostStatus**: `MLSZKSZPlatform::types::PostStatus` -- DRAFT(0), PUBLISHED(1), EXPIRED(2), DELETED(3), PENDING_REVIEW(4)
- **AnnouncementStatus**: `MLSZKSZPlatform::types::AnnouncementStatus` -- DRAFT(0), PUBLISHED(1), DELETED(2)
- Both share the DRAFT->PUBLISHED->DELETED core lifecycle
- PostStatus extends with EXPIRED and PENDING_REVIEW for moderated content
- Transfer objects (News, Offer, Request, Announcement) expose publish/delete/edit operations

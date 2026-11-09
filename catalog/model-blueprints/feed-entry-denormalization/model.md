## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::FeedEntry`
  - Attributes: entryType (req), contentId (req), createdAt (req), title, summary, organizationName, capabilities, authorName, validUntil, isSensitive, validFrom
  - Relations: post (0..1 ASSOC), ownerOrganization (1..1 ASSOC), targetOrganizations (0..* ASSOC)
  - Non-CRUD; populated by backend syncFeed operation
- **Transfer Object**: `MLSZKSZPlatform::services::feed::FeedEntryTO`
  - Adds relations to specific content type TOs: request (0..1), offer (0..1), news (0..1), announcement (0..1), organization (1..1)
- Organization has both ownedFeedEntries and feedEntries relations for owned vs targeted content

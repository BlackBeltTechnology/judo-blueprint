## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::Organization`
  - Attributes: name (req), contactEmail (req), status (req), cityName, fullAddress, contactName, contactPhone, logo, membershipStart, membershipDescription, isUserCountHidden (default: false), isAdminOrganization (default: false), userCount
  - Relations: address (0..1 COMPOSITION), capabilities (0..* ASSOC), users (0..* ASSOC), news (0..* ASSOC), offers (0..* ASSOC), requests (0..* ASSOC), ownedFeedEntries (0..* ASSOC), feedEntries (0..* ASSOC), post (0..* ASSOC), invitations (0..* COMPOSITION)
- **OrganizationStatus enum**: `MLSZKSZPlatform::types::OrganizationStatus` -- ACTIVE(0), SUSPENDED(1), DEACTIVATED(2)

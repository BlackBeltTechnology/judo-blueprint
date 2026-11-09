## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::User`
  - Attributes: name (req), email (req), role (req), status (req), isVisible (default: true), isSilentMode, emailNotifications, organizationName, notifyOffers (default: true), notifyRequests (default: true), notifyAnnouncements (default: true), notifyNews, lastLogin
  - Relations: organization (1..1), inquiries (0..*), devices (0..*), notifications (0..*)
- **UserRole enum**: `MLSZKSZPlatform::types::UserRole` -- COMPANY_ADMIN(0), COMPANY_READER(1), PLATFORM_ADMIN(2), ASSOCIATION_LEADERSHIP(3)
- **UserStatus enum**: `MLSZKSZPlatform::types::UserStatus` -- ACTIVE(0), SUSPENDED(1), DEACTIVATED(2)
- Transfer objects project different views: admin::CompanyUser (with activate/deactivate/suspend ops), companyreader::ProfilePanel (notification prefs), technical::User (access control flags)

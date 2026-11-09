## Examples

### sanctuary-backend
- **Enum**: `Sanctuary::user::PrivacyVisibility` -- publicForPeers(1), publicForTeam(2), publicForUnit(3), publicForEveryone(4)
- **UserPrivacySettings entity**: `Sanctuary::user::UserPrivacySettings` (createable/updateable/deleteable)
  - Attributes (all typed to PrivacyVisibility):
    - phoneNumber -- controls visibility of the user's phone number
    - peerBadges -- controls visibility of peer-awarded badges
    - specialBadges -- controls visibility of special badges
    - systemBadges -- controls visibility of system-awarded badges
- The UserPrivacySettings entity is composed (owned) by the User entity via a [0..1] COMPOSITION relation
- The corresponding `UserPrivacySettingsTO` transfer object is the only TO in this model with CRUD flags enabled, allowing direct privacy settings management through the API
- The enum ordinals (1-4) represent expanding visibility scope, enabling range-based queries (e.g., "show to anyone with visibility level >= publicForTeam")

## Examples

### sanctuary-backend
**Entity types (all in Sanctuary::user package):**

- **User**: `Sanctuary::user::User` (createable/updateable/deleteable)
  - Attributes: email (Email), title (String), firstName (String), lastName (String), sex (String), profilePhoto (String), status (ActiveStatus), phoneNumber (Phone)
  - Relations:
    - privacySettings [0..1] COMPOSITION -> UserPrivacySettings
    - settings [0..1] COMPOSITION -> UserSettings
    - roles [0..*] ASSOCIATION -> Role (bidirectional, partner=users)
    - roleGroups [0..*] ASSOCIATION -> RoleGroup (bidirectional, partner=users)
    - positionTitle [0..1] ASSOCIATION -> PositionTitle
    - effectiveRoles [0..*] ASSOCIATION -> Role (DERIVED: `self.roles`)

- **Role**: `Sanctuary::user::Role` (createable/updateable/deleteable)
  - Attributes: name (String)
  - Relations: users [0..*] ASSOCIATION -> User (bidirectional, partner=roles)

- **RoleGroup**: `Sanctuary::user::RoleGroup` (createable/updateable/deleteable)
  - Attributes: name (String)
  - Relations:
    - roles [0..*] ASSOCIATION -> Role (one-way)
    - users [0..*] ASSOCIATION -> User (bidirectional, partner=roleGroups)

- **PositionTitle**: `Sanctuary::user::PositionTitle` (createable/updateable/deleteable)
  - Attributes: title (String), status (ActiveStatus)

- **UserPrivacySettings**: `Sanctuary::user::UserPrivacySettings` (createable/updateable/deleteable)
  - Attributes: phoneNumber (PrivacyVisibility), peerBadges (PrivacyVisibility), specialBadges (PrivacyVisibility), systemBadges (PrivacyVisibility)

- **UserSettings**: `Sanctuary::user::UserSettings` (createable/updateable/deleteable)
  - Attributes: darkMode (Boolean)

**Enumerations:**
- `Sanctuary::user::PrivacyVisibility`: publicForPeers(1), publicForTeam(2), publicForUnit(3), publicForEveryone(4)
- `Sanctuary::ActiveStatus`: active(1), archived(2)

**Transfer objects (all mapped, in Sanctuary::user):**
- `UserTO` [maps User] -- all entity attributes + relations to RoleTO, RoleGroupTO, PositionTitleTO, UserPrivacySettingsTO (AGGREGATION), UserSettingsTO (AGGREGATION), effectiveRoles
- `RoleTO` [maps Role] -- name
- `RoleGroupTO` [maps RoleGroup] -- name + roles [0..*] ASSOCIATION to RoleTO
- `PositionTitleTO` [maps PositionTitle] -- title, status
- `UserPrivacySettingsTO` [maps UserPrivacySettings] -- phoneNumber, peerBadges, specialBadges, systemBadges (createable/updateable/deleteable)
- `UserSettingsTO` [maps UserSettings] -- darkMode

**Actor:**
- `Sanctuary::Admin` (anonymous, human, realm=DEFAULT, managed=true)
  - accesses: users [0..*] -> UserTO (full CRUD), roles [0..*] -> RoleTO (full CRUD), roleGroups [0..*] -> RoleGroupTO (full CRUD), positionTitles [0..*] -> PositionTitleTO (full CRUD)
  - Menu items: UsersMenu, RolesMenu, RoleGroupsMenu, PositionTitlesMenu

**Notable features:**
- The model has several empty placeholder packages (unit, article, project, faq) suggesting the project is in early development with planned expansion
- The `effectiveRoles` derived relation currently only resolves to `self.roles` (direct assignments), not yet incorporating roles from RoleGroups
- The UserPrivacySettingsTO is the only transfer object with CRUD flags enabled (createable/updateable/deleteable), allowing direct privacy settings management

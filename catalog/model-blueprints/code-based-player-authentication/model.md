## Examples

### trivia
- **User entity** (`trivia::entities::User`): non-CRUD
  - Attributes: email (req), name (req), active (req, default: true), code (optional), tmpCode (optional)
  - Relations: tests (0..* ASSOC to Test)
  - Operations: reset (INSTANCE) -- regenerates the access code
- **Admin entity** (`trivia::entities::Admin`): non-CRUD
  - Attributes: email (req), active (req, default: true)
  - Separate entity for admin actors (not the same as User)
- **RegisterInput TO** (`trivia::actors::player::RegisterInput`): unmapped
  - Attributes: email (req), name (optional)
  - Used as input for the register operation
- **Credential TO** (`trivia::actors::player::Credential`): unmapped
  - Attributes: code (req), email (req)
  - Used as input for the activate operation -- validates the code sent to the player's email
- **Player Application TO** (`trivia::actors::player::Application`):
  - Attributes: name (optional)
  - Operations: register (STATIC), activate (STATIC)
  - Entry point for the player registration/authentication flow
- **Admin User TO** (`trivia::actors::admin::User`):
  - Attributes: email (req), name (req), active (req), code, tmpCode
  - Operations: reset (MAPPED) -- admin can reset a player's code
- **Two actor types**: Admin (`trivia::actors::admin::Admin`) and Player (`trivia::actors::player::Player`)
  - Admin manages questions, contests, users; Player registers, enters contests, takes tests
- **AdminPrincipal TO** (`trivia::actors::admin::AdminPrincipal`): email (req), active (req) -- the logged-in admin's identity

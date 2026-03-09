## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%ErrorCode%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%BusinessError%" } }) {
  items { fqn name _type mapping { fqn }
    attributes { items { name } }
  }
} } }
```

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%DeclarationError%" } }) {
  items { fqn name _type mapping { fqn }
    attributes { items { name } }
  }
} } }
```

```graphql
{ esm { transferobjecttypes(where: { name: { eq: "Error" } }) {
  items { fqn name _type mapping { fqn }
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "ErrorCode"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ErrorCode", name: "{{ERROR_CODE_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "BusinessError"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::BusinessError", name: "errorCode"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::BusinessError", name: "message"
} }) { success fqn } }
```

## Examples

### indamedia-adtrack
- **ErrorCode enum**: `AdTrack::entities::ErrorCode` -- 12 members:
  - CLIENT_NOT_FOUND(1), USER_NOT_FOUND(2), PERMISSION_DENIED(3), ACCOUNT_NOT_FOUND(4), CAMPAIGN_NOT_FOUND(5), CREDENTIAL_NOT_SET(6), CREDENTIAL_NOT_FOUND(7), CONNECTION_FAILD(8), TRACKED_CAMPAIGN_NOT_FOUND(9), TRACKED_CAMPAIGN_UNFETCHABLE(10), PLATFORM_NOT_SUPPORTED(11), PLATFORM_NOT_IMPLEMENTED(12)
- **BusinessError TO**: `AdTrack::services::BusinessError` (unmapped)
  - Attributes: errorCode (optional), message (optional)
  - Used as output of custom operations to communicate domain-level failures
- Error codes cover: entity lookup failures (*_NOT_FOUND), authorization (PERMISSION_DENIED), integration issues (CONNECTION_FAILD, CREDENTIAL_NOT_SET), and platform support (PLATFORM_NOT_SUPPORTED, PLATFORM_NOT_IMPLEMENTED)

### park-here
- **ErrorCode enum**: `ParkHere::entities::ErrorCode` -- 8 members:
  - PERMISSION_DENIED(1), USER_NOT_FOUND(2), MISSING_REQUIRED_DATA(3), NOT_VALID_DATA(4), RESERVATION_NOT_FOUND(5), TOO_MANY_RESERVATION(6), CAR_NOT_FOUND(7), CONFIGURATION_NOT_FOUND(8)
- **BusinessError TO**: `ParkHere::services::BusinessError` (unmapped)
  - Attributes: errorCode (req), message (req) -- both required in this variant
- Error codes cover: authorization (PERMISSION_DENIED), entity lookup failures (USER_NOT_FOUND, RESERVATION_NOT_FOUND, CAR_NOT_FOUND, CONFIGURATION_NOT_FOUND), validation (MISSING_REQUIRED_DATA, NOT_VALID_DATA), and business rules (TOO_MANY_RESERVATION)
- Shares PERMISSION_DENIED and USER_NOT_FOUND codes with indamedia-adtrack, confirming these as universal error conditions

### ubives
- **ErrorCode enum**: `Ubives::entities::ErrorCode` -- 20 members covering identity management domain:
  - ORGANIZATION_ALREADY_EXISTS_WITH_THIS_NAME(1), ACCOUNT_IS_ALREADY_IN_ORGANIZATION(2), APPLICATION_ALREADY_EXISTS_IN_ORGANIZATION_WITH_THIS_NAME(3), ACCOUNT_DOES_NOT_EXISTS(4), ORGANIZATION_DOES_NOT_EXISTS(5), IDENTITY_DOES_NOT_EXISTS(6), FACE_IDENTIDIER_DOES_NOT_EXISTS(7), USER_DOES_NOT_EXISTS(8), ORGANIZATION_ACCESS_DOES_NOT_EXISTS(9), REALM_DOES_NOT_EXISTS(10), APPLICATION_DOES_NOT_EXISTS(11), INVITATION_DOES_NOT_EXISTS(12), IDM_DOES_NOT_EXISTS(13), PASSWORD_DOES_NOT_MATCH(14), KEYCLOAK_USER_ALREADY_EXISTS_WITH_THIS_NAME(15), KEYCLOAK_CLIENT_ALREADY_EXISTS_WITH_THIS_NAME(16), KEYCLOAK_COULD_NOT_CREATE_USER(17), KEYCLOAK_COULD_NOT_CREATE_CLIENT(18), USER_ALREADY_EXISTS_IN_ORGANIZATION_WITH_THIS_NAME(19), MISSING_REQUIRED_ATTRIBUTE(10000)
- **BusinessError TO**: `Ubives::entities::BusinessError` (unmapped)
  - Attributes: code (req), message (req) -- uses `code` instead of `errorCode`
- Error codes cover: uniqueness violations (*_ALREADY_EXISTS*), entity lookup failures (*_DOES_NOT_EXISTS), authentication (PASSWORD_DOES_NOT_MATCH), Keycloak integration (KEYCLOAK_*), and validation (MISSING_REQUIRED_ATTRIBUTE at ordinal 10000, placed far from domain errors)
- Notable: uses `code` field name instead of `errorCode`, and the BusinessError TO is in the entities package rather than a services package

### workflow-poc
- **DeclarationErrorCode enum**: `workflow::transfers::DeclarationErrorCode` -- 1 member:
  - INVALID_REFERENCE(1)
- **DeclarationError TO**: `workflow::transfers::admin::DeclarationError` (unmapped)
  - Attributes: code (req), message (optional)
- Domain-scoped variant: the error code enum is specific to workflow declaration validation (checking that workflow YAML references valid states and transitions) rather than general application errors
- Uses `code` field name (like ubives) rather than `errorCode`
- Minimal starter enum with a single member, expected to grow as more validation rules are added

### trivia
- **ErrorCode enum**: `trivia::actors::player::ErrorCode` -- 5 members:
  - INVALID_CODE(1), CONTEST_NOT_OPEN(2), TEST_NOT_STARTED(3), TEST_ALREADY_STARTED(4), TEST_CLOSED(5)
- **Error TO**: `trivia::actors::player::Error` (unmapped)
  - Attributes: code (req), message (optional)
- Actor-scoped variant: the ErrorCode enum lives in the player actor namespace rather than the shared entities package, meaning error codes are specific to the player-facing API
- Error codes cover: authentication/validation (INVALID_CODE), state violations (CONTEST_NOT_OPEN, TEST_NOT_STARTED, TEST_ALREADY_STARTED, TEST_CLOSED)
- Uses simplified TO name `Error` instead of `BusinessError`, and `code` field name (like ubives and workflow-poc)
- All error codes relate to quiz workflow state preconditions: the player must use a valid code, the contest must be open, the test must be in the right state

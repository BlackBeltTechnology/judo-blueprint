## Examples

### InterfaceRegister
- **Enum**: `InterfaceRegister::entities::Environment` -- DEV(1), TEST(2), PROD(3)
- Used as a required attribute on `ApplicationInstance` entity: environment (Environment, req)
- ApplicationInstance represents a deployed instance of an Application in a specific environment
- The enum enables tracking which environments an application has been deployed to, supporting enterprise operations management workflows
- Other environment-adjacent enums in the same model: `DevelopmentType` (COTS, COTS_WITH_ADDITIONAL_DEVELOPMENTS, CUSTOM_DEVELOPMENT, UNKNOWN) classifies how the application was built

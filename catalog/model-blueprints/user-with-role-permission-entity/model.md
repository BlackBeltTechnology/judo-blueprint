## Examples

### rackinspect
- **User entity**: `rackinspect::entities::User` (non-CRUD)
  - Attributes (28): name (req), email (req), active (default: true), notes, rolesString, plus 23 denormalized permission booleans (permissionToCompanyData, permissionToConfiguration, permissionToDocumentRegistry, permissionToExchangeRates, permissionToPartners, permissionToPaymentDeadlines, permissionToPaymentMethods, permissionToRoles, permissionToUnits, permissionToUsers, permissionToFaultRegistries, permissionToOffers, permissionToItems, permissionToRepairCategories, permissionToDimensionTemplates, permissionToErrorCategories, permissionToRackElements, permissionToRackTypes, permissionToBrands, permissionToRepairTypes, permissionToErrorDestinations, permissionToErrorCodes, permissionToErrorQualifications)
  - Relations: roles (0..* ASSOC to Role), permissions (0..* DERIVED), userAddresses/userEmails/userPhones (0..* COMPOSITION), primaryUserAddress/primaryUserEmail/primaryUserPhone (0..1 ASSOC), tasks (0..* ASSOC)
  - Operations: toggleActive, recalculatePermissions (custom), createExchangeRate, updateExchangeRateForDateInterval
- **Role entity**: `rackinspect::entities::Role` -- name (req), permissions (0..* ASSOC to Permission)
- **Permission entity**: `rackinspect::entities::Permission` -- flag (req), id (req)
- **PermissionFlag enum**: `rackinspect::entities::PermissionFlag` -- 23 members: FAULT_REGISTRIES(1), OFFERS(2), ITEMS(3), REPAIR_CATEGORIES(4), DIMENSION_TEMPLATES(5), ERROR_CATEGORIES(6), RACK_ELEMENTS(7), RACK_TYPES(8), PARTNERS(9), BRANDS(10), REPAIR_TYPES(11), ERROR_DESTINATIONS(12), EXCHANGE_RATES(13), USERS(14), ERROR_CODES(15), ERROR_QUALIFICATIONS(16), UNITS(17), PAYMENT_METHODS(21), COMPANY_DATA(25), ROLES(26), PAYMENT_DEADLINES(28), CONFIGURATION(29), DOCUMENT_REGISTRY(31)

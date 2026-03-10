## Detection Query

```graphql
{ esm { entitytypes(limit: 100) {
  items { fqn name
    attributes { items { name defaultExpression } totalCount }
    relations { totalCount }
  }
} } }
```

Look for entities with 1-2 attributes (name, or name + active/isEnabled) and few or no relations.

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{LOOKUP_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{LOOKUP_NAME}}", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{LOOKUP_NAME}}", name: "{{ENABLED_FLAG}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{LOOKUP_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{LOOKUP_NAME}}", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{LOOKUP_NAME}}", name: "{{ENABLED_FLAG}}"
} }) { success fqn } }
```

## Examples

### reserve-app
Eight entities follow the name+active reference data pattern:
- **Gate**: `ReserveApp::entities::Gate` -- name (req), active (default: true); relation: freightReservations (0..* ASSOC)
- **VehicleType**: `ReserveApp::entities::VehicleType` -- name (req), active (default: true); no relations
- **LoadingType**: `ReserveApp::entities::LoadingType` -- name (req), active (default: true); no relations
- **Spot**: `ReserveApp::entities::Spot` -- name (req), active (default: true); relations: projects (0..* ASSOC), freightReservations (0..* ASSOC)
- **ProductCategory**: `ReserveApp::entities::ProductCategory` -- name (req), active; no relations
- **Unit**: `ReserveApp::entities::Unit` -- name (req), active; no relations
- **StorageType**: `ReserveApp::entities::StorageType` -- name (req), active; no relations
- **LoadingTime**: `ReserveApp::entities::LoadingTime` -- name (req), minutes, active (default: true); extended variant with a minutes attribute

All are non-CRUD entities. Transfer objects in `ReserveApp::services` mirror the entity structure for admin management, while role-specific TOs (e.g., `GateForPartner`, `SpotForPartner`) expose only the name for partner-facing views.

### alba
Three entities follow the name+isEnabled reference data pattern:
- **Audience**: `Alba::entities::Audience` -- name (req), isEnabled (default: true); no relations
- **Curriculum**: `Alba::entities::Curriculum` -- name (req), isEnabled (default: true); no relations
- **ResultType**: `Alba::entities::ResultType` -- name (req), isEnabled (default: true); no relations

All are non-CRUD entities. Referenced by Product via 0..* ASSOCIATION relations (audience, curriculum, resultTypes). Transfer objects exist in both admin and author views:
- `Alba::services::Audience` / `Alba::services::AudienceTransfer` -- name (+ isEnabled in full view, name-only in simplified)
- `Alba::services::Curriculum` / `Alba::services::CurriculumTransfer` -- name (+ isEnabled in full view)
- `Alba::services::ResultType` / `Alba::services::ResultTypeTransfer` -- name (+ isEnabled in full view)
- Used in product form TOs (AuthorProductForm, AdminProductForm) as AGGREGATION relations for multi-select

Also **Institution**: `Alba::entities::Institution` -- name (req), address, isEnabled (default: true), website; relation: teachers (0..* ASSOC to User). An extended variant adding address and website fields, plus a collection relation to teachers at the institution.

### trivia
One entity follows the name-only reference data pattern (simplest variant, no active/enabled flag):
- **Category**: `trivia::entities::Category` -- name (req); relation: questions (0..* ASSOC to Question)

Non-CRUD entity. Referenced by Question via `category` (0..1 ASSOC) and by Contest via `categories` (0..* ASSOC) for filtering which question categories a contest draws from.
- **Admin Category TO** (`trivia::actors::admin::Category`): name (req), nrOfQuestions (optional) -- adds a derived count attribute showing how many questions belong to this category
- The simplest variant: no active/enabled flag, just a name for classification

### itracker
Two entities follow the name-only reference data pattern (simplest variant, no active/enabled flag):
- **Region**: `itracker::entities::Region` -- name (req); no relations, no operations
- **SRTCategory**: `itracker::entities::SRTCategory` -- name (req); no relations, no operations

Both are non-CRUD entities. Referenced by Initiative via 1..1 ASSOCIATION relations (region, category). Transfer objects in `itracker::actors::user` mirror the entity with name-only structure (Region TO, SRTCategory TO).
- Region represents geographic classification of cost-saving initiatives
- SRTCategory represents strategic sourcing category classification
- Both are seeded via the Application.init operation and serve as dropdown selections when creating initiatives

### viterra_demo
One entity follows the name-only reference data pattern with a localization extra attribute:
- **Commodity**: `viterra::Commodity` -- name (req), hun (optional); no relations, no operations

Non-CRUD entity. Referenced by Stock via `commodity` (1..1 ASSOC). The `hun` attribute stores a Hungarian translation of the commodity name, making this a localized variant of the name-only reference data pattern.
- **CommodityTransfer TO**: `viterra::CommodityTransfer` -- name (MAPPED), hun (MAPPED); direct projection of the entity
- Seeded via Application.init with 7 commodity entries (barley and corn variants)
- Accessed by Admin actor via `commodities` access point (createable, updateable)

### InterfaceRegister
Two entities follow the reference data lookup pattern:
- **Brand**: `InterfaceRegister::entities::Brand` -- name (req, identifier); no relations, no operations
  - Simplest variant: name-only lookup with no active/enabled flag
  - Non-CRUD entity, seeded via Initializer.initBrands
  - **BrandTransfer TO**: `InterfaceRegister::enterpriseArchitect::BrandTransfer` -- name (req, MAPPED); direct projection
  - Accessed by EnterpriseArchitect actor via `brands` access point (createable, not updateable/deleteable)
  - Referenced by HighLevelConnection via `brands` (0..* ASSOC) for tagging connections by brand

- **BusinessDataType**: `InterfaceRegister::entities::BusinessDataType` -- name (req, identifier), businessDomain (req, BusinessDomain enum); no relations, no operations
  - Extended variant: adds a `businessDomain` enum classifier (CRM, FINANCE, NEW_VEHICLE_SALES, AFTER_SALES) alongside the name
  - Non-CRUD entity, seeded via Initializer.initBusinessDataTypes
  - **BusinessDataTypeTransfer TO**: `InterfaceRegister::enterpriseArchitect::BusinessDataTypeTransfer` -- name (req, MAPPED), businessDomain (req, MAPPED)
  - Accessed by EnterpriseArchitect actor via `businessDataTypes` access point (createable, updateable)
  - Referenced by HighLevelConnection via `businessDataTypes` (0..* ASSOC) for categorizing connections by data type

### doors-model
Six entities follow the reference data lookup pattern:
- **Role**: `doors::entities::Role` -- name (req); relation: positions (0..* ASSOC to Position bidirectional)
  - Simple name-only lookup representing organizational roles (e.g., "Kontrolling osztalyvezeto", "Penzugyi igazgato", "Vezerigazgato")
  - Referenced by Position via `role` (1..1 ASSOC) and by Stage/WorkflowStage via `responsible` (1..1 ASSOC) for workflow stage assignment

- **Bank**: `doors::entities::Bank` -- name (req, identifier), giroCode (req, identifier)
  - Extended variant: adds a `giroCode` attribute as a bank identifier code (e.g., "120" for Raiffeisen)
  - Referenced by BankAccount via `bank` (0..1 ASSOC)
  - Seeded via init data with Hungarian bank names and codes

- **LegalGroup**: `doors::entities::LegalGroup` -- name (req, identifier); relation: categories (0..* ASSOC to LegalCategory bidirectional)
  - Grouping entity for legal categories, forming a two-level legal classification hierarchy

- **LegalCategory**: `doors::entities::LegalCategory` -- code (LegalCode, req, identifier), name (req, identifier); relation: group (1..1 ASSOC to LegalGroup bidirectional)
  - Code+name variant with a foreign key to LegalGroup, forming a grouped lookup

- **FinancialCategory**: `doors::entities::FinancialCategory` -- code (FinancialCode, req, identifier), name (req, identifier); no relations
  - Code+name variant for financial classification

- **Division**: `doors::entities::Division` -- code (DivisionCode, req, identifier), name (req, identifier); relations: positions (0..* ASSOC to Position), contracts (0..* ASSOC to Contract)
  - Code+name variant representing organizational divisions, referenced by both Position and Contract entities

All are non-CRUD entities, seeded via the Initializer.init operation. The admin actor manages Divisions, Positions, and Banks via dedicated access points. The employee actor views Roles and Categories through mapped transfer objects for contract type selection.

### ams-model
One entity follows the identifier+name reference data lookup pattern:
- **Application**: `ams::entities::Application` -- identifier (req, identifier), name (req); relations: requests [0..*] ASSOC Request (bidirectional), admin [0..1] ASSOC User (bidirectional)
  - Identifier+name variant representing IT systems/applications (e.g., CM, PLM, SAP, PTIC, VITRIN)
  - Non-CRUD entity, seeded via User.init operation
  - Referenced by Request (abstract) via `application` [1..1] ASSOCIATION, and by Campaign via `applications` [0..*] ASSOCIATION
  - The identifier serves as a short code (e.g., "CM") while name is the display name (e.g., "CM")
  - **Admin Application TO** (`ams::actors::admin::Application`): identifier (MAPPED, req), name (MAPPED, req) -- full CRUD management by Admin actor
  - **Admin Campaign TO** shows applications via AGGREGATION relation (DERIVED from campaign.applications)
  - Accessed by Admin actor via `applications` access point (createable, updateable, deleteable)

### kozut-eugyfel-client
Three entities follow the reference data lookup pattern with Hungarian naming (megnevezes = designation/name):
- **Megye (County)**: `e_ugyfelszolgalat::entities::Megye` -- megnevezes (req, identifier); relation: felhasznalok (users 0..* TwoWay ASSOC to Felhasznalo)
  - Simple name-only lookup representing Hungarian counties for geographic assignment of workers
  - Referenced by Felhasznalo (User) via `megye` (0..1 TwoWay ASSOC)
  - Managed by Admin actor via `megyek` access point

- **SzervezetiEgysegTipus (Organizational Unit Type)**: `e_ugyfelszolgalat::entities::SzervezetiEgysegTipus` -- megnevezes (req, identifier); no relations
  - Simple name-only lookup representing types of organizational units (e.g., road maintenance center, bridge office)
  - Referenced by Felhasznalo (User) via `szervezetiEgysegTipus` (0..1 OneWay ASSOC)
  - Managed by Admin actor via `szervezetiEgysegTipusok` access point

- **Munkakor (Job Role)**: `e_ugyfelszolgalat::entities::Munkakor` -- megnevezes (req, identifier); no relations
  - Simple name-only lookup representing job roles within the organization
  - Referenced by Felhasznalo (User) via `munkakor` (0..1 OneWay ASSOC)
  - Note: The MunkakorEnum (Ugyfelszolgalati_Munkatars, Szervezetiegyseg_Vezeto, Szervezetiegyseg_Munkatars) exists as a parallel enum but the Munkakor entity provides the configurable lookup for admin management

All three use `megnevezes` (Hungarian for "designation") instead of `name` as the primary identifier attribute -- a localized variant of the name-only reference data pattern. All are managed by the Admin actor and serve as organizational classification for workers.

### skillmatrix-model
Five entities follow the reference data lookup pattern:
- **Country**: `SkillMatrix::Country` -- code (req, identifier); no relations, no operations
  - Simplest code-only variant representing nationalities
  - Referenced by User via `nationality` (0..1 OneWay ASSOC)
  - Transfer object: hrEmployee::Country (code MAPPED)

- **Language**: `SkillMatrix::Language` -- code (req, identifier); no relations, no operations
  - Simplest code-only variant representing languages
  - Referenced by LanguageSkill via `language` (1..1 OneWay ASSOC)
  - Transfer object: hrEmployee::Language (code MAPPED)

- **Job**: `SkillMatrix::Job` -- title (req, identifier); no relations, no operations
  - Name-only variant (using `title` instead of `name`) representing job titles
  - Referenced by Resume via `job` (0..1 OneWay ASSOC)

- **Tag**: `SkillMatrix::Tag` -- name (req, identifier); relations: competences (0..* TwoWay ASSOC Competence), users (0..* DERIVED User)
  - Name-only variant serving as a classification tag for competences
  - Many-to-many relationship with Competence via TwoWay ASSOCIATION
  - Users are derived through competence linkage
  - Transfer objects: hrEmployee::Tag (name MAPPED), report::Tag (used in reporting)

- **SkillLevel**: `SkillMatrix::SkillLevel` -- name (req), score (req); no relations, no operations
  - Extended variant with a `score` numeric attribute for ranking skill proficiency levels
  - Referenced by Skill via `approvedLevel` and `requestedLevel` (0..1 OneWay ASSOC), and by SkillTarget via `skillLevel` (1..1 OneWay ASSOC)
  - Transfer objects: hrEmployee::SkillLevel (name, score MAPPED), manager::SkillLevel (name MAPPED), professional::SkillLevel (used in skill display)
  - Represents proficiency tiers (e.g., Beginner=1, Intermediate=2, Advanced=3, Expert=4) with names and numeric scores

### mlszksz-platform
Three entities follow the reference data lookup pattern with name + isActive flag:
- **City**: `MLSZKSZPlatform::entities::City` -- name (req, default: ""), isActive (req, default: true); relation: postalCodes (0..* ASSOC to PostalCode)
  - Name + isActive variant representing cities in a geographic lookup hierarchy
  - Non-CRUD entity (createable=false, updateable=false, deleteable=false)
  - Referenced by Address via `city` (1..1 ASSOC)
  - Paired with PostalCode in a bidirectional city-postalCode reference data hierarchy
  - Admin TO (`MLSZKSZPlatform::services::admin::City`): name, isActive + postalCodes relation + activateToggle and updateCity operations
  - CompanyAdmin TO (`MLSZKSZPlatform::services::companyadmin::City`): name + postalCodes relation (read-only view, no operations)

- **Capability**: `MLSZKSZPlatform::entities::Capability` -- name (req), description (optional), isActive (req, default: true); no relations
  - Extended name + description + isActive variant representing organizational capabilities/tags
  - CRUD entity (createable=true, updateable=true, deleteable=true)
  - Referenced by Organization, Offer, Request, and RegistrationRequest via `capabilities` (0..* ASSOC) for tagging
  - Admin TO (`MLSZKSZPlatform::services::admin::Capability`): name, description, isActive + activateToggle and updateCapability operations
  - Feed TO (`MLSZKSZPlatform::services::feed::Capability`): name, description, isActive (read-only)

- **PostalCode**: `MLSZKSZPlatform::entities::PostalCode` -- code (req); relation: cities (0..* ASSOC to City)
  - Code-only variant (no name or active flag) representing postal codes
  - CRUD entity (createable=true, updateable=true, deleteable=true)
  - Referenced by Address via `postalCode` (1..1 ASSOC)
  - The City-PostalCode pair forms a bidirectional geographic reference data hierarchy, where a PostalCode can belong to multiple cities and a city can have multiple postal codes

All seeded via the Initializer.init operation. The `isActive` flag name is unique to this project (other projects use `active`, `isEnabled`, or no flag).

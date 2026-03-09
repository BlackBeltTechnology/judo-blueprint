## Detection Query

```graphql
{ esm { actortypes(limit: 10) {
  items { fqn name }
  totalCount
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { eq: "Role" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

```graphql
{ esm { transferobjecttypes(limit: 100) {
  items { fqn name }
} } }
```

Look for multiple actor types combined with transfer objects named `<Entity>For<Role>` or `<Role><Entity>`.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "Role"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Role", name: "{{ROLE_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "User",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "role"
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{ROLE_NAME}}User"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{ROLE_NAME}}User", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{ROLE_NAME}}User", name: "role"
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{ENTITY_NAME}}For{{ROLE_NAME}}"
} }) { success fqn } }
```

## Examples

### reserve-app
- **Role enum**: `ReserveApp::entities::Role` -- PARTNER(1), LOGISTICIAN(2), DOORMAN(3), READ_ONLY(4), ADMIN(5)
- **5 Actor types**: AdminActor, PartnerActor, LogisticianActor, DoormanActor, Readonly
- **User entity**: `ReserveApp::entities::User` (non-CRUD)
  - Attributes: email (req), firstName, lastName, fullName, phone, role (Role enum)
  - Relations: projects (0..* ASSOC), company (0..1 ASSOC), partner (0..1 ASSOC)
  - Operations: init (STATIC) for data seeding
- **Per-role User TOs** (all mapping the same User entity):
  - `AdminUser` -- email (req), firstName, fullName, lastName, phone, role, fixFalse (admin-only flag)
  - `PartnerUser` -- email (req), firstName, fullName, lastName, phone, role
  - `LogisticianUser` -- email (req), firstName, fullName, lastName, phone, role
  - `DoormanUser` -- email (req), firstName, fullName, lastName, phone, role
  - `ReadonlyUser` -- email (req), firstName, fullName, lastName, phone, role
- **Per-role entity TOs** (partner role examples):
  - `ReservationForPartner` -- 18 attributes; denormalized fields: projectAsString, recipientAsString, gateAsString, spotAsString, duration, durationHuman; relations via AGGREGATION
  - `ProjectForPartner` -- name only
  - `GateForPartner` -- name only
  - `SpotForPartner` -- name only
  - `CompanyForPartner` -- name only
  - `PartnerForPartner` -- address, contact, name, phone (no externalIdentifier or active flag)
  - `LoadingTypeForPartner` -- name only
  - `VehicleTypeForPartner` -- name only
- **Admin full-entity TOs**: StorageType, Unit, Project, ProductCategory, Spot, Gate, Partner, Company, LoadingType, VehicleType, LoadingTime, ManagedUser -- each exposing all entity attributes including the active flag
- **ManagedUser TO**: Full user management view with company (0..1), projects (0..*), partner (0..1) relations for admin user administration

### viterra_demo
- **2 Actor types**: Admin (anonymous, full access), Partner (principal=ClientTransfer, self-service)
- **No Role enum** -- roles are implicit in the actor type definitions rather than stored on an entity
- **Client entity** serves as the "user" for the Partner actor (principal=ClientTransfer, claim: EMAIL)
- **Admin actor accesses** (all as ALL access type, createable+updateable):
  - periods (0..* PeriodTransfer), silos (0..* SiloTransfer), clients (0..* ClientTransfer), commodities (0..* CommodityTransfer), reports (0..* ReportTransfer)
- **Partner actor accesses** (all as DERIVED access type, read-only):
  - openReports (0..* PartnerOpenReportTransfer) -- filtered by `status == PENDING and client.email == getVariable("ACTOR", "email")`
  - closedReports (0..* PartnerClosedReportTransfer) -- filtered by `status != PENDING and client.email == getVariable("ACTOR", "email")`
  - partnerData (0..1 PartnerClientTransfer) -- single client record matching logged-in email
- **Report entity projected differently per actor**:
  - Admin sees `ReportTransfer`: status, clientId, clientName, displayPeriodName, reportingStartTime, reportingFinishTime + client/period/stocks AGGREGATION relations
  - Partner sees `PartnerOpenReportTransfer` (for PENDING): displayPeriodName, clientName, reportingStartTime, reportingFinishTime + stocks (editable)
  - Partner sees `PartnerClosedReportTransfer` (for SUBMITTED): same fields but read-only stocks
- **Stock entity projected differently per actor**:
  - Admin sees `StockTransfer`: totalQuantity, isccQuantity, contract + silo/commodity AGGREGATION relations
  - Partner sees `PartnerOpenStockTransfer`: contract (DERIVED), reportedQuantity, reportedIsccQuantity, moisture, temperature, infestation, notes (MAPPED for editing) + commodityHun, siloName, siloPlace (DERIVED denormalized)
- The naming convention is `Partner<Context><Entity>Transfer` rather than `<Entity>For<Role>`

### doors-model
- **2 Actor types**: Admin (realm: DOORS_ADMIN, managed, non-anonymous), Employee (realm: DOORS_USER, anonymous, principal=EmployeePrincipal, isActiveExpression: self.active)
- **No Role enum** -- instead, roles are managed through a Role entity referenced by Position (organizational role system)
- **Admin actor** (`doors::actors::admin::Admin`):
  - Accesses: companies (0..*), employees (0..*), divisions (0..*), positions (0..*), banks (0..*) -- all with full CRUD
  - 5 menu items for entity management
  - TOs in admin package: Company (extensive: 17 attributes including derived bank/fullAddress/signerName, relations to signer/bankAccounts/mainBankAccount), Employee (7 attributes + positions relation), Division (code, name), Position (assignmentUpperLimit + role/division/employees/assignee/openStages relations), Bank (name, giroCode), BankAccount (accountNumber + bank/partner/ownerCompany relations)
- **Employee actor** (`doors::actors::employee::Employee`):
  - Principal: EmployeePrincipal TO (maps Employee entity with name, email, active, isAdmin, positions -- self-referencing principal)
  - Uses `isActiveExpression: self.active` for authentication filtering
  - Accesses: companies, contractTypes, contracts, partners, myContracts, myInitiatives, selectedCompany, profile, selectedContractType -- mix of ALL and DERIVED access types
  - Key TOs in employee package:
    - Contract (extensive: 30+ attributes, 15+ relations, 15+ operations including approve, reject, sign, close, startApproval, uploadFile, generateDocument, validate, addComment)
    - ContractForAction (simplified: 12 attributes for action views, approve/reject/sign operations)
    - ContractType (12 attributes + legalCategory/financialCategory relations, createContract/createContractWithTemplate/createContractWithoutTemplate operations)
    - Company/CompanySelect (full and simplified views)
    - Partner/PartnerSelect (full and selection views with generalization hierarchy: PrivatePartner, OrganizationPartner, SelfEmployedPartner, OtherPartner)
    - Address, BankAccount, Bank, Comment, ContractLog, Division/DivisionSelect
  - Derived accesses use `getVariable("ACTOR", "email")` for filtering: myContracts filters by signee, myInitiatives filters by officer
- **Key differences from other projects**:
  - Admin vs Employee separation: Admin manages organizational structure (companies, employees, divisions, positions, banks); Employee works with contracts and partners
  - Employee actor is anonymous with principal-based authentication (realm=DOORS_USER, isActiveExpression for filtering)
  - No Role enum; organizational roles are managed through the Position entity that links Employee + Role + Division
  - Same entities exposed with vastly different TOs: admin Company has 17 attributes while employee CompanySelect has only 3

### ams-model
- **2 Actor types**: Manager (realm: AMS, principal=User, anonymous=true, managed=true, isActiveExpression: `self.subordinates!count() > 0`), Admin (realm: AMS, principal=Admin, anonymous=true, managed=true)
- **No Role enum** -- roles are implicit in the actor type definitions; the Manager actor is restricted to users who have subordinates via isActiveExpression
- **User entity** (`ams::entities::User`) serves as the principal for the Manager actor (claim: USERNAME on email)
- **Admin entity** (`ams::entities::Admin`) serves as the principal for the Admin actor (claim: EMAIL on email)
- **Manager actor** (`ams::actors::manager::Manager`):
  - Accesses: subordinates (0..* DERIVED: self.subordinates), approvalAll (0..1 DERIVED: self), approvalList (0..* DERIVED: filtered by campaignStatus==OPEN, dashboard annotation)
  - 3 menu items: subordinates (people icon), approvalAll (done_all icon, "Approve All Pending"), approvalList (done icon)
  - TOs in manager package:
    - Subordinate (maps User): identifier, firstName, lastName, fullName -- simplified read-only user view
    - Request (maps ConfirmationRequest): applicationName, userName, userEmail, responsibleName, status, type, loginName, effectiveDate, isPending, roles, campaignStatus + approve/reject operations
    - ManagerApprovalList (maps User): approvals [0..*] AGGREGATION Request (DERIVED, filtered: pending + open campaign) + approveAll operation
- **Admin actor** (`ams::actors::admin::Admin`):
  - Accesses: campaigns (0..* ALL, full CRUD), applications (0..* ALL, full CRUD), users (0..* ALL, read-only)
  - 3 menu items: users (people icon), applications (apps icon), campaigns (done_all icon)
  - TOs in admin package:
    - ConfirmationRequest (maps ConfirmationRequest): applicationName, loginName, userName, effectiveDate, userEmail, roles, status, responsibleName -- read-only detail view (no approve/reject)
    - Campaign (maps Campaign): startDate, finishDate, status, download (DERIVED), ratio (DERIVED progress), isOpen/isClosed/isEmpty (guard attributes) + confirmationRequests/applications AGGREGATION + close/open/load operations
    - Application (maps Application): identifier, name -- full CRUD management
    - User (maps User): lastName, firstName, email -- read-only listing
- **Same entities projected differently per actor**:
  - ConfirmationRequest: Manager sees it as "Request" with approve/reject operations and isPending guard; Admin sees it as "ConfirmationRequest" with read-only detail fields and no operations
  - User: Manager sees subordinates as "Subordinate" (identifier, firstName, lastName, fullName); Admin sees all users as "User" (lastName, firstName, email)
  - Campaign: Only visible to Admin actor with full management operations; Manager sees only the filtered approval requests from open campaigns
- **Key differences from other projects**:
  - Manager actor uses `isActiveExpression: self.subordinates!count() > 0` to restrict access to users who manage others (unique activation criteria based on relation count)
  - Two separate principal entities: User (for Manager) and Admin (for Admin), rather than a single User entity serving both actors
  - The Manager actor has a dual-purpose view: individual request approval (approvalList) and bulk approval (approvalAll with approveAll operation)
  - The dashboard annotation is applied to the campaigns access (Admin) and approvalList access (Manager) for landing page display

### kozut-eugyfel-client
- **3 Actor types**: Admin (`e_ugyfelszolgalat::actors::admin::Admin`), Munkatars (`e_ugyfelszolgalat::actors::munkatars::Munkatars`), EUgyfelAlkalmazas (`e_ugyfelszolgalat::actors::eUgyfelAlkalmazas::EUgyfelAlkalmazas`)
- **No Role enum** -- roles are managed through a MunkakorEnum (job role enum: Ugyfelszolgalati_Munkatars, Szervezetiegyseg_Vezeto, Szervezetiegyseg_Munkatars) but actors are separate types, not driven by this enum
- **Felhasznalo (User) entity** (`e_ugyfelszolgalat::entities::Felhasznalo`):
  - Attributes: email (req, identifier), vezetekNev, keresztNev, nev (DERIVED), admin (boolean), cimke (DERIVED label), and multiple DERIVED role flags: ugyfelszolgalatiMunkatars, szervezetiEgysegMunkatars, szervezetiEgysegVezeto
  - Relations: feladatok (tasks 0..*), szervezetiEgysegTipus (0..1), ertesitesek (notifications 0..*), bejelentesek (reports 0..*), megye (county 0..1), munkakor (job role 0..1)
- **Admin actor**:
  - Accesses: erkeztetok (dispatchers), szervezetiEgysegTipusok (org unit types), megyek (counties), felhasznalok (users), szinkronizaltSzervezetek (synced orgs), bejelentesek (reports)
  - 6 menu items for managing reference data, users, dispatchers, and synchronization
  - TOs: AdminPrincipal (email, nev), admin::Erkezteto (bejelentesTipus, felelosCimke, felelos relation), admin::Bejelentes (azonosito, letrehozasIdopont, allapot, felelosNev, ugyintezoNev + felelos/ugyintezo relations) -- summary list view with status
- **Munkatars (Worker) actor**:
  - Accesses: feladatok (tasks), ertesitesek (notifications), aktivBejelentesek (active reports), lezartBejelentesek (closed reports), olvasottErtesitesek (read notifications), tovabbitas (forwarding)
  - TOs: MunkatarsPrincipal (extensive: cimke, email, admin, vezetekNev, keresztNev, nev, munkakorNev, megyeNev, szervezetiEgysegTipusNev + megye/szervezetiEgysegTipus/munkakor relations)
  - munkatars::BejelentesMegtekinto -- full detail view with 23 attributes including permission guard booleans (lezarasEngedely, megjegyzesEngedely, tovabbitasEngedely, tovabbitasFelelosnekEngedely, resztvevoHozzadasEngedely, megnyitasEngedely, leiratkozasEngedely) + 7 mapped operations (megjegyzes, lezaras, megnyitas, tovabbitas, tovabbitasFelelosnek, hozzaadResztvevo, leiratkozas) + tovabbitasok/esemenyek/resztvevok/kepek relations
  - munkatars::Ertesites (notification view with elolvas/markRead operation)
- **EUgyfelAlkalmazas (external e-service app) actor**:
  - Accesses: bejelentes (single report access)
  - TOs: eUgyfelAlkalmazas::Bejelentes -- minimal view with display attribute + letrehoz (create) STATIC operation
- **Same Bejelentes entity projected 3 ways**:
  - Admin sees summary list (azonosito, allapot, felelosNev, ugyintezoNev)
  - Munkatars sees full detail (all attributes + 7 permission guards + 7 operations + 4 relations)
  - EUgyfelAlkalmazas sees creation-only view (display, letrehoz static operation)
- **Key differences from other projects**:
  - Three distinct actor tiers: admin (reference data management), worker (case handling with rich permission guards), external application (API-level creation only)
  - No customer-facing actor -- the EUgyfelAlkalmazas is a machine/application actor, not a human user
  - Permission guards are DERIVED boolean attributes on the entity (not on the TO), computed from the ticket's state and the current user's role
  - Organizational structure (Megye/county + SzervezetiEgysegTipus/org unit type + Munkakor/job role) determines which operations a worker can perform on a ticket

### skillmatrix-model
- **4 Actor types**: AdminActor (`actor::admin::AdminActor`), UserActor (`actor::admin::UserActor`), HREmployeeActor (`actor::hrEmployee::HREmployeeActor`), ProfessionalActor (`actor::professional::ProfessionalActor`)
- **No Role enum** -- roles are determined by boolean flags on the User entity: isActiveAdmin, isActiveHREmployee, isActiveProfessional. A hidden ManagerActor is implied by the manager package TOs
- **User entity** (`SkillMatrix::User`):
  - Attributes: email (req, identifier), firstName, lastName, title, phone, dateOfBirth, fullName (DERIVED), indexName (DERIVED), isActiveAdmin (req), isActiveHREmployee (req), isActiveProfessional (req), isInactiveUser (DERIVED), hasApprovalRequest (DERIVED), hasSkills (DERIVED)
  - Relations: unit (0..1 TwoWay ASSOC Unit), nationality (0..1 ASSOC Country), skills (0..* TwoWay ASSOC Skill), languageSkills (0..* COMPOSITION LanguageSkill), resumes (0..* COMPOSITION Resume), managedUnits (0..* TwoWay ASSOC Unit), subordinates (0..* DERIVED User), trainingPlans (0..* COMPOSITION TrainingPlan), skillTargets (0..* DERIVED SkillTarget), searches (0..* ASSOC Search)
  - Operations: initializer, deleteUser, approveAllSkills, approveAllSubordinatesSkills, createTrainingPlan, completeAllTargets
- **4 actor packages with role-specific TOs**:
  - **admin** -- User management: admin::Admin (email, isActiveAdmin), admin::User (14 attributes including all role flags; operations: deleteUser, createTestData)
  - **hrEmployee** -- Competence/skill administration: hrEmployee::HREmployee (email, isActiveAdmin), hrEmployee::Professional (8 identity attributes + languages/nationality/unit/skills relations), hrEmployee::Competence (name, strategic, active, hasReferences, notActive + tags relation; operations: delete), hrEmployee::Unit (name + unitMembers/unitManager relations), hrEmployee::Search (name + result/tags/competences/professionals relations; operations: run), hrEmployee::SkillLevel (name, score), hrEmployee::Tag (name)
  - **professional** -- Self-assessment: professional::Professional (email, fullName, dateOfBirth, phone + 3 DERIVED display attributes), professional::MyProfessional (skills, skillTargets relations), professional::Skill (approved, competenceName, requestedLevelName + competence/approvedLevel/requestedLevel relations), professional::SkillTarget (competenceName, targetLevel, deadline)
  - **manager** -- Subordinate management: manager::Subordinate (lastTrainingPlanDate, indexName + trainingPlans/skills/targetSkills relations; operations: approveAllSkills, createTrainingPlan, completeAllTargets), manager::Skill (competenceName, approvedLevel, requestedLevel, approved, professionalName, unapproved; operations: approve), manager::TrainingPlan (closed, date, description, isOpen, subordinateName + skillTargets/notes relations; operations: close, open), manager::SkillTarget (competenceName, completed, deadline, skillLevelName + competence/skillLevel relations), manager::UnapprovedSkillsView (skillsToApprove relation; operations: approveAllSubordinatesSkills)
- **Same entities projected differently per actor**:
  - User: Admin sees full user management (14 attributes, deleteUser/createTestData); HREmployee sees Professional (8 identity attributes + domain relations); Professional sees personal profile (7 read-only attributes); Manager sees Subordinate (2 attributes + 3 relations + 3 operations)
  - Skill: HREmployee sees approved status + competenceName + level; Professional sees approved/competenceName/requestedLevelName + 3 relations; Manager sees full approval context (6 attributes + approve operation)
  - Competence: HREmployee sees full admin view (5 attributes + delete); Manager sees read-only name; Professional sees read-only name (via Skill.competence relation)
- **Key differences from other projects**:
  - Boolean role flags on User entity replace Role enum (isActiveAdmin, isActiveHREmployee, isActiveProfessional)
  - Manager role is implicit (determined by managedUnits relationship, not a boolean flag)
  - Deep per-actor specialization: the manager actor has unique Subordinate/TrainingPlan/UnapprovedSkillsView TOs not present in other actor views
  - The HREmployee acts as the domain administrator for competences, skills, and search, while Admin handles only user account management

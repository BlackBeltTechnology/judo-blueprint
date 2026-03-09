## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "User" } }) {
  items { fqn name
    attributes { items { name required } totalCount }
  }
} } }
```

Look for User entities with multiple boolean attributes following the `is<RoleName>` or `isActive<RoleName>` naming pattern.

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "User",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "firstName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "lastName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "phone"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "created"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "is{{ROLE_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "CreateUserInput"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::CreateUserInput", name: "has{{ROLE_NAME}}Access"
} }) { success fqn } }
```

## Examples

### InterfaceRegister
- **User entity**: `InterfaceRegister::entities::User` (createable=true, updateable=true, deleteable=true)
  - Identity attributes: firstName (String, req), lastName (String, req), email (Email, req, identifier), phone (Phone)
  - Timestamp: created (Timestamp)
  - Boolean role flags (all required):
    - isAdmin (Boolean, req)
    - isEnterpriseArchitect (Boolean, req)
    - isDeveloper (Boolean, req)
    - isOperator (Boolean, req)
  - Operations: createApplication (INSTANCE), createHighLevelConnection (INSTANCE), createUser (INSTANCE) -- all model-defined, stateful
  - No role relations or role enums -- each role is a direct boolean on the entity

- **User TO**: `InterfaceRegister::enterpriseArchitect::User` [maps User]
  - All entity attributes directly mapped: firstName, lastName, email, phone, created, isAdmin, isEnterpriseArchitect, isDeveloper, isOperator

- **CreateUserInput TO** (unmapped): `InterfaceRegister::enterpriseArchitect::CreateUserInput`
  - Transient attributes: email (req), firstName (req), lastName (req), phone
  - Boolean flags renamed: hasAdminAccess (req), hasEnterpriseArchitectAccess (req), hasDeveloperAccess (req), hasOperatorAccess (req)
  - Uses `has...Access` naming convention instead of `is...` for input clarity

- **Dashboard TO**: `InterfaceRegister::enterpriseArchitect::Dashboard` [maps User]
  - The Dashboard maps to the User entity, providing a createUser operation that takes CreateUserInput and produces User TO

### skillmatrix-model
- **User entity**: `SkillMatrix::User` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Identity attributes: email (Email, req, identifier, default: 'info@bb.hu'), firstName (String), lastName (String), title (String), phone (Phone), dateOfBirth (Date)
  - Derived display: fullName (DERIVED: `self.firstName + ' ' + self.lastName`), indexName (DERIVED: `self.lastName + ', ' + self.firstName`)
  - Boolean role flags (all required, all default: false):
    - isActiveAdmin (Boolean, req, default: false)
    - isActiveHREmployee (Boolean, req, default: false)
    - isActiveProfessional (Boolean, req, default: false)
  - Derived role check: isInactiveUser (DERIVED: `not (self.isActiveAdmin or self.isActiveHREmployee or self.isActiveProfessional)`)
  - Domain-specific derived flags: hasApprovalRequest (DERIVED: `not self.skills!filter(s | not s.approved)!empty()`), hasSkills (DERIVED: `not self.skills!empty()`)
  - Relations: unit (0..1 TwoWay ASSOC Unit), nationality (0..1 OneWay ASSOC Country), skills (0..* TwoWay ASSOC Skill), languageSkills (0..* COMPOSITION LanguageSkill), resumes (0..* COMPOSITION Resume), resumeLists (0..* OneWay ASSOC ResumeList), managedUnits (0..* TwoWay ASSOC Unit), subordinates (0..* DERIVED User), trainingPlans (0..* COMPOSITION TrainingPlan), skillTargets (0..* DERIVED SkillTarget), incompleteSkillTargets (0..* DERIVED SkillTarget), lastTrainingPlan (0..1 DERIVED TrainingPlan), searches (0..* OneWay ASSOC Search)
  - Operations: initializer, deleteUser, approveAllSkills, approveAllSubordinatesSkills, createTrainingPlan, completeAllTargets
  - Uses `isActive<RoleName>` naming convention with explicit default of false

- **4 Actor types** correspond to the 3 boolean roles plus a user management actor:
  - AdminActor -- maps to admin::Admin TO (email DERIVED, isActiveAdmin MAPPED)
  - UserActor -- maps to admin::User TO (full user management with deleteUser, createTestData operations)
  - HREmployeeActor -- maps to hrEmployee::HREmployee TO (email DERIVED, isActiveAdmin MAPPED)
  - ProfessionalActor -- maps to professional::Professional TO (personal profile view)

- **Per-actor User TOs** (all projecting the same User entity with different field sets):
  - admin::User -- 14 attributes including all role flags, fullName, indexName, isInactiveUser, hasSkills; operations: deleteUser, createTestData (custom)
  - hrEmployee::Professional -- 8 attributes: email, lastName, firstName, title, fullName, phone, dateOfBirth, indexName; relations: languages, nationality, unit, skills
  - professional::Professional -- 7 attributes: email, fullName, dateOfBirth, phone, unit (DERIVED), manager (DERIVED), nationality (DERIVED)

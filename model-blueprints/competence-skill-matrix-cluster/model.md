## Detection Query

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name } }
    relations { items { name memberType relationKind } }
  }
} } }
```

Look for entities named Competence, Skill, SkillLevel, or SkillTarget with relations between them.

## Creation Mutations

### Competence entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Competence",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Competence", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Competence", name: "strategic"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Competence", name: "active"
} }) { success fqn } }
```

### SkillLevel entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "SkillLevel",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::SkillLevel", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::SkillLevel", name: "score"
} }) { success fqn } }
```

### Skill entity (junction with dual level references)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Skill",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Skill", name: "competence",
  target: "{{NAMESPACE}}::Competence", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Skill", name: "approvedLevel",
  target: "{{NAMESPACE}}::SkillLevel", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Skill", name: "requestedLevel",
  target: "{{NAMESPACE}}::SkillLevel", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Skill", name: "user",
  target: "{{NAMESPACE}}::User", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Skill", name: "approve",
  operationType: "INSTANCE", binding: "INSTANCE"
} }) { success fqn } }
```

### SkillTarget entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "SkillTarget",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::SkillTarget", name: "completed"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::SkillTarget", name: "deadline"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::SkillTarget", name: "skillLevel",
  target: "{{NAMESPACE}}::SkillLevel", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::SkillTarget", name: "competence",
  target: "{{NAMESPACE}}::Competence", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

## Examples

### skillmatrix-model
- **Competence entity**: `SkillMatrix::Competence`
  - Attributes: name (req, identifier), strategic (req, default: false), active (req, default: true)
  - Relations: skills (0..* TwoWay ASSOC Skill), tags (0..* TwoWay ASSOC Tag), users (0..* DERIVED User), skillTargets (0..* TwoWay ASSOC SkillTarget)
  - Operations: delete (INSTANCE)
  - The `users` DERIVED relation navigates through skills to find all users with this competence

- **SkillLevel entity**: `SkillMatrix::SkillLevel`
  - Attributes: name (req), score (req)
  - No relations, no operations
  - Referenced by Skill (approvedLevel, requestedLevel) and SkillTarget (skillLevel)

- **Skill entity**: `SkillMatrix::Skill`
  - Stored attributes: none (all data is in relations)
  - Derived attributes: approvedLevelName (`self.approvedLevel.name`), requestedLevelName (`self.requestedLevel.name`), approved (`self.approvedLevel!isDefined() and self.requestedLevel!isDefined() and self.approvedLevel == self.requestedLevel`), competenceScore (`self.approvedLevel.score`), competenceName (`self.competence.name`), userFullName (`self.user.fullName`), unitName (`self.user.unit.name`)
  - Relations: competence (1..1 TwoWay ASSOC Competence), approvedLevel (0..1 OneWay ASSOC SkillLevel), requestedLevel (0..1 OneWay ASSOC SkillLevel), user (0..1 TwoWay ASSOC User)
  - Operations: approve (INSTANCE) -- copies requestedLevel to approvedLevel

- **SkillTarget entity**: `SkillMatrix::SkillTarget`
  - Attributes: completed (Boolean), deadline (Date)
  - Relations: skillLevel (1..1 OneWay ASSOC SkillLevel), competence (1..1 TwoWay ASSOC Competence)
  - Owned by TrainingPlan via COMPOSITION

- **User entity**: `SkillMatrix::User`
  - Relations: skills (0..* TwoWay ASSOC Skill), trainingPlans (0..* COMPOSITION TrainingPlan), skillTargets (0..* DERIVED SkillTarget), incompleteSkillTargets (0..* DERIVED SkillTarget)
  - Operations: approveAllSkills, approveAllSubordinatesSkills, createTrainingPlan, completeAllTargets
  - Derived: hasApprovalRequest (`not self.skills!filter(s | not s.approved)!empty()`)

- **Tag entity**: `SkillMatrix::Tag`
  - Attributes: name (req, identifier)
  - Relations: competences (0..* TwoWay ASSOC Competence), users (0..* DERIVED User)
  - Tags provide a flexible classification overlay on competences

- **Transfer object projections per actor**:
  - hrEmployee::Competence -- full admin view (name, strategic, active, hasReferences, notActive + tags; delete operation)
  - hrEmployee::Skill -- read-only skill view (competenceName, levelName, approved + competence/approvedLevel)
  - professional::Skill -- self-assessment view (approved, competenceName, requestedLevelName + competence/approvedLevel/requestedLevel)
  - manager::Skill -- approval view (competenceName, approvedLevel, requestedLevel, approved, professionalName, unapproved; approve operation)
  - manager::SkillTarget -- training goal view (competenceName, completed, deadline, skillLevelName + competence/skillLevel)

- **LanguageSkill entity**: `SkillMatrix::LanguageSkill` -- a parallel skill entity for language proficiency
  - Attributes: level (LanguageSkillLevel enum: BEGINNER/CONVERSATIONAL/FLUENT/NATIVE), note (Text)
  - Relations: language (1..1 OneWay ASSOC Language)
  - Owned by User via COMPOSITION
  - Uses an enum for levels instead of a SkillLevel entity reference, reflecting the standardized CEFR-like proficiency scale

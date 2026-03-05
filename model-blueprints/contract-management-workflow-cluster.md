---
id: contract-management-workflow-cluster
title: "Contract Management with Workflow Approval Stages"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - doors-model
---

## Description

A comprehensive contract management entity cluster centered around a Contract entity with a multi-stage approval workflow engine. The core entities are:

- **Contract** -- the main entity representing a contract document with extensive attributes (title, status, netValue, kind, role, signDate, creationDate, registrationNumber, version, year, sequence, file, signedFile, and multiple boolean flags). The Contract progresses through a status lifecycle: CREATED -> PENDING -> APPROVED -> SIGNED -> CLOSED (with REJECTED as a branch from PENDING). Operations include startApproval, approve, reject, sign, close, validate, uploadFile, uploadSignedContract, generateDocument, and workflow management helpers (setNextStage, setResponsible, addSignee, addLog).

- **ContractType** -- a classification entity for contracts with code, name, title, and boolean flags (isSpecial, isTemplateBased, isFinancialSpecial, isLegalSpecial) plus a template attribute. References LegalCategory and FinancialCategory for regulatory classification. Has factory operations (createContract, createContractWithTemplate, createContractWithoutTemplate) for contract creation.

- **Workflow** -- a named workflow definition entity that owns WorkflowStage entries via composition.

- **Stage** (abstract base) -- defines workflow stage structure: name, order, activityType (StageType enum: COMMENT/APPROVE), responsible (Role), and condition attributes (conditionNetValueUpperLimit, conditionNetValueLowerLimit, conditionTemplateBased, conditionSpecial, conditionFinancialSpecial, conditionLegalSpecial using StageCondition enum: DONTCARE/EXECUTE/SKIP).

- **WorkflowStage** -- extends Stage; owned by Workflow as a template definition of stages.

- **ContractStage** -- extends Stage; owned by Contract as runtime instances of stages. Adds autoApproved, completed, rejected boolean attributes, a comment field, and responsiblePositions/pendingContract relations. Created by copying WorkflowStage templates when startApproval is invoked.

- **ContractLog** -- an event log entity composed by Contract, recording timestamp, user, event (ContractEvent enum: CREATED/SIGNED/CLOSED/UPLOADED), sequence number, and file version snapshots (contractVersion, signedContractVersion).

- **Comment** -- a simple text+timestamp+user entity composed by Contract for rejection comments.

Key structural patterns:
- Template/instance pattern: WorkflowStage is a template; ContractStage is its runtime copy
- Generalization: both WorkflowStage and ContractStage extend the abstract Stage entity
- Condition-based routing: stage conditions determine whether a stage is EXECUTE'd, SKIP'd, or DONTCARE'd based on contract attributes
- Position-based authorization: each stage references responsible Positions who can approve
- Auto-approval: stages that do not match conditions are automatically approved, advancing the workflow
- Document generation: contracts can have their documents generated from templates via backend code

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Contract%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%Workflow%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    generalizations { items { fqn } }
  }
} } }
```

Look for a Contract entity with approve/reject/sign operations and a composed stages relation, alongside Workflow/WorkflowStage/ContractStage entities.

## Creation Mutations

### Contract entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Contract",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Contract", name: "title"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Contract", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Contract", name: "netValue"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Contract", name: "creationDate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Contract", name: "signDate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Contract", name: "file"
} }) { success fqn } }
```

### DocumentStatus enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "DocumentStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DocumentStatus", name: "CREATED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DocumentStatus", name: "PENDING", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DocumentStatus", name: "APPROVED", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DocumentStatus", name: "SIGNED", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DocumentStatus", name: "REJECTED", ordinal: 5
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DocumentStatus", name: "CLOSED", ordinal: 6
} }) { success fqn } }
```

### Stage (abstract base)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Stage",
  createable: false, updateable: false, deleteable: false, abstract: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Stage", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Stage", name: "order"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Stage", name: "activityType"
} }) { success fqn } }
```

### WorkflowStage and ContractStage (extend Stage)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "WorkflowStage",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::WorkflowStage",
  target: "{{NAMESPACE}}::Stage"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "ContractStage",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::ContractStage",
  target: "{{NAMESPACE}}::Stage"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ContractStage", name: "completed"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ContractStage", name: "rejected"
} }) { success fqn } }
```

### Workflow entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Workflow",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Workflow", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Workflow", name: "stages",
  target: "{{NAMESPACE}}::WorkflowStage", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

### Contract relations

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Contract", name: "stages",
  target: "{{NAMESPACE}}::ContractStage", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Contract", name: "workflow",
  target: "{{NAMESPACE}}::Workflow", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Contract operations

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Contract", name: "startApproval",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Contract", name: "approve",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Contract", name: "reject",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Contract", name: "sign",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Contract", name: "close",
  operationType: INSTANCE
} }) { success fqn } }
```

## Examples

### doors-model
**Entity types (all in doors::entities package):**

- **Contract**: `doors::entities::Contract` (non-CRUD)
  - Attributes (20): title, status (DocumentStatus, default: CREATED), kind (ContractKind, req, default: CREATION), role (ContractRole, req, default: PURCHASER), netValue (Long), creationDate (Date, default: now()), signDate, financialAprvDate, financialAprvName, legalAprvDate, legalAprvName, registrationNumber, version (Integer), year (Integer), sequence (Integer), file (ContractTemplate), signedFile (SignedContract), isSpecial (Boolean, req, default: false), isTemplateBased (Boolean, req, default: false), forceSpecial, forceSpecialAvailable, isSuitableForGeneration
  - Relations (15): stages [0..*] COMPOSITION ContractStage, contractLogs [0..*] COMPOSITION ContractLog, comments [0..*] COMPOSITION Comment, contract_AE99 [0..1] COMPOSITION Contract_AE99, contractType [1..1] ASSOC ContractType (bidirectional), contractor [1..1] ASSOC Company (bidirectional), partner [1..1] ASSOC Partner, signee [0..1] ASSOC Employee (bidirectional), officer [1..1] ASSOC Employee (bidirectional), division [1..1] ASSOC Division (bidirectional), workflow [0..1] ASSOC Workflow, openStage [0..1] ASSOC ContractStage (bidirectional), lastApprover [0..1] ASSOC Employee, contractorBankAccount [0..1] DERIVED (self.contractor.mainBankAccount), partnerBankAccount [0..1] DERIVED (self.partner.mainBankAccount)
  - Operations (14): startApproval (output: StartApprovalResult), approve, reject (input: RejectInput), sign, close, setNextStage, setResponsible, addSignee, validate (custom, output: ValidateContractResult), addLog (input: ContractLog), generateDocument (custom), updateDocument, uploadFile (custom, input: UploadFileInput), uploadSignedContract (custom, input: UploadSignedFileInput)

- **Workflow**: `doors::entities::Workflow` (non-CRUD)
  - Attributes: name (req)
  - Relations: stages [0..*] COMPOSITION WorkflowStage

- **Stage**: `doors::entities::Stage` (non-CRUD, base entity for WorkflowStage and ContractStage)
  - Attributes: name (req), order (Integer, req), activityType (StageType, req, default: APPROVE), conditionNetValueUpperLimit (Integer, req, default: -1), conditionNetValueLowerLimit (Integer, req, default: 0), conditionSpecial (StageCondition, req, default: DONTCARE), conditionTemplateBased (StageCondition, req, default: DONTCARE), conditionFinancialSpecial (StageCondition, req, default: DONTCARE), conditionLegalSpecial (StageCondition, req, default: DONTCARE)
  - Relations: responsible [1..1] ASSOC Role

- **WorkflowStage**: `doors::entities::WorkflowStage` (non-CRUD, extends Stage)
  - No additional attributes or relations beyond Stage

- **ContractStage**: `doors::entities::ContractStage` (non-CRUD, extends Stage)
  - Additional attributes: autoApproved (Boolean), completed (Boolean, req, default: false), rejected (Boolean, req, default: false), comment (Text)
  - Additional relations: responsiblePositions [0..*] ASSOC Position (bidirectional), pendingContract [0..1] ASSOC Contract (bidirectional)

- **ContractType**: `doors::entities::ContractType` (non-CRUD)
  - Attributes: name (req), code (req, identifier), title, isSpecial (Boolean, req, default: false), isTemplateBased (Boolean, req, default: false), isFinancialSpecial (Boolean), isLegalSpecial (Boolean), template (ContractTypeTemplate)
  - Relations: legalCategory [1..1] ASSOC LegalCategory, financialCategory [1..1] ASSOC FinancialCategory, contracts [0..*] ASSOC Contract (bidirectional)
  - Operations: createContract (custom, input: CreateContractInputTO, output: CreateContractResult), createContractWithTemplate (custom, input/output), createContractWithoutTemplate (custom, input/output), init (STATIC)

- **ContractLog**: `doors::entities::ContractLog` (non-CRUD)
  - Attributes: timestamp (Timestamp, req), user (String, req), event (ContractEvent, req), sequence (Integer), contractVersion (ContractTemplate), signedContractVersion (SignedContract)

- **Comment**: `doors::entities::Comment` (non-CRUD)
  - Attributes: text (Text), timestamp (Timestamp, req), user (String, req)

**Enumerations:**
- `DocumentStatus`: CREATED(1), PENDING(2), APPROVED(3), SIGNED(4), REJECTED(5), CLOSED(6)
- `ContractKind`: CREATION(1), MODIFICATION(2), TERMINATION(3)
- `ContractRole`: PURCHASER(1), SUPPLIER(2), BARTER(3)
- `ContractPeriod`: FIXED_DATE(1), INFINITE(3), FIXED_TO_INFINITE(4)
- `ContractPerformance`: SINGLE(1), CONTINUOUS(2)
- `StageType`: COMMENT(1), APPROVE(2)
- `StageCondition`: DONTCARE(1), EXECUTE(2), SKIP(3)
- `ContractEvent`: CREATED(1), SIGNED(3), CLOSED(6), UPLOADED(7)
- `Currency`: HUF(1), EUR(2), USD(3)
- `PartnerType`: FREELANCE(1), RESIDENT_ENTERPRISE(2), FOREIGN_ENTERPRISE(3), FOUNDATION(4), ORGANIZATION(5), GOVERMENT(6), OTHER(7)

**Workflow lifecycle:**
1. ContractType.createContract creates a new Contract with status=CREATED
2. Contract.startApproval validates the contract, transitions to PENDING, copies WorkflowStages into ContractStages, and begins stage processing
3. Contract.setNextStage evaluates conditions and either auto-approves or assigns responsible Positions
4. Contract.approve completes the current stage and advances to the next
5. Contract.reject marks the current stage as rejected and sets status to REJECTED (can be restarted)
6. Contract.sign transitions from APPROVED to SIGNED
7. Contract.close transitions from SIGNED to CLOSED

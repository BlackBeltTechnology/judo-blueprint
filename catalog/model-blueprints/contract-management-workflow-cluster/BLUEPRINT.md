---
id: "contract-management-workflow-cluster"
title: "Contract Management with Workflow Approval Stages"
score: 32.0
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

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

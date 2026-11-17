---
id: contract-management-workflow-cluster
title: Contract Management with Workflow Approval Stages
description: A contract entity with a multi-stage approval workflow, where workflow stage templates are copied into runtime stages on the contract when approval starts.
aliases: [contract approval workflow, staged approval, contract stages]
keywords: [contract, workflow, approval, stage, template, runtime copy, abstract stage, generalization]
tags: ["domain:model", "layer:model", "project:doors-model", "status:single-project"]
category: pattern
status: single-project
projects: [doors-model]
evidence: ["doors-model:unrecorded"]
alternatives: [product-with-approval-workflow, approval-workflow-pattern]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Run a contract through a sequence of approval stages defined once as a workflow. Each contract gets its own copy of the stages when approval starts, so later changes to the template do not alter a contract already in review.

### Workflow stages are templates, contract stages are copies

The workflow owns its stage templates. Starting approval copies each template onto the contract as a runtime stage. The contract then tracks its own progress through those copies.

### Stage kinds share one abstract base

Workflow stages and contract stages both extend one abstract Stage (an entity with `abstract = true` that cannot be instantiated directly and must be subclassed). The common fields (name, order, activity type) are defined once. Each kind adds only what it needs.

## Structure

The Contract entity has a title (required), a status (required, from the ContractStatus enumeration), a net value and a sign date. It owns a list of contract stages through a composition and refers to at most one Workflow (0..1). It has operations to start approval, approve and reject.

The ContractStatus enumeration has six values: created, pending, approved, signed, closed and rejected.

The Workflow entity has a name (required) and owns its workflow stages through a composition.

The abstract Stage has a name (required), an order (required) and an activity type (required, from the StageType enumeration with the values comment and approve). WorkflowStage and ContractStage both extend it. ContractStage adds flags for auto-approved, completed and rejected.

## Constraints

- A contract stage is created from a workflow stage only when approval starts. The contract never changes the template.
- Stages are ordered by their order value. Two stages of one workflow do not share an order.
- The status moves forward through the stages and reaches rejected only from pending. The enumeration does not enforce this; the operations do.
- Interceptors do not run for custom operations (platform behaviour), so they do not run for the approval operations. Each one must check the current status and the caller's role. A refused transition is a business fault, which the operation must declare in its `faults`, or the generated interface has no matching `throws` clause.
- The contract owns its runtime stages by composition, so deleting a contract deletes its stages. The link to the Workflow is an association and cascades nothing. Copying templates into runtime stages is common practice, not a platform feature.
- A stage that does not match the contract's conditions is approved automatically and does not wait for a person.

## Variations

- **Conditions per stage.** A stage can run, skip or be ignored depending on contract attributes such as the net value. Add condition fields to the template and evaluate them when the runtime stage is created.
- **Position-based approval.** Each stage names the role or position allowed to approve it. Check that role in the approve operation.
- **Comment stage.** A stage with the comment activity type records a comment and does not block the workflow.

## When to use

- A document needs a fixed sequence of approvals that can differ by workflow.
- Each document must keep a record of the stages it went through, even if the template later changes.
- Approvers are chosen by role or position for each stage.

## When to avoid

- The approval path is a single step. Use one approve operation without stages.
- The sequence is decided by the people involved, not by a template. Use free-form review with comments.
- The workflow must branch and loop with many guards. Use a state machine with transitions instead.

## Related

- [[approval-workflow-pattern]]: the general pattern for an approval that someone signs off
- [[product-with-approval-workflow]]: an approval workflow on a product, a simpler form of the same need
- [[document-review-state-machine]]: a review of a document with explicit state transitions
- [[content-lifecycle-status-enum]]: a status enumeration used for lifecycle values
- [[safe-failure-pattern]]: keeping the audit record when a stage side effect fails

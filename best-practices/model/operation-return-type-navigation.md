---
id: "operation-return-type-navigation"
title: "Operation Return Type for View Navigation"
domain: "model"
category: "operation"
score: 32.3
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - viterra_demo
  - workflow-poc
---
## Description

A state-transition operation returns a transfer object of a different type than the current view, causing the UI framework to automatically navigate to the appropriate view for the returned type. This is used when an entity's state change means it should no longer appear in the current list/view and should instead appear in a different partition.

## Structure

- Entity operation changes status and returns `this` (the entity itself)
- The operation's output parameter targets a different transfer object type than the caller's type
- The framework automatically maps the returned entity to the output transfer type
- The UI navigates from the current view to the output view
- Example flow: Partner editing an open report -> submits -> status changes -> returns closed report transfer -> UI redirects to closed reports view

```
// Entity operation
Report.submit():
  this.status = ReportStatus#SUBMITTED
  return this

// Output type is PartnerClosedReportTransfer (not PartnerOpenReportTransfer)
output: PartnerClosedReportTransfer [1..1]
```

## Examples

### Viterra Demo
`Report.submit()` sets status to SUBMITTED and returns `this`. The output type is `PartnerClosedReportTransfer` (not `PartnerOpenReportTransfer`). When the partner submits from the open report view, the framework converts the returned entity to a closed report transfer, and the UI redirects to the closed reports view. The report disappears from "Open reports" and appears in "Closed reports".

### workflow-poc
The workflow engine uses a redirect pattern for post-operation navigation. `Token.navigate()` returns a `UpdateRedirect` transfer (mapped from Context) containing `actor`, `access`, `idValue`, `idName` attributes that instruct the UI where to navigate. `User.startWorkflow()` returns a `CreateRedirect` transfer (mapped from ContextType) with `actor`, `access`, `operation` attributes. These redirect TOs encapsulate navigation metadata rather than returning the entity itself, enabling the workflow engine to dynamically direct users to arbitrary views.

## Trade-offs

- Pros: Seamless post-transition navigation, no client-side routing logic needed, declarative view routing through return types
- Cons: Return type must be carefully chosen to match the target view, only works for single-entity returns
- Prefer when: A state transition moves an entity from one logical partition to another and the user should see the new view immediately

## Related Patterns

- [state-based-transfer-partitioning](state-based-transfer-partitioning.md)
- [mapped-operation-delegation](mapped-operation-delegation.md)
- [enum-state-machine](enum-state-machine.md)

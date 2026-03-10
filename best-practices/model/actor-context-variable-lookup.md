---
id: "actor-context-variable-lookup"
title: "Actor Context Variable Lookup Pattern"
domain: "model"
category: "access"
score: 47.4
usage_count: 7
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - alba
  - viterra_demo
  - judo-demo-miniworkflow
  - InterfaceRegister
  - judo-partner
  - workflow-poc
---
## Description

Operations and derived access expressions use `TypeName!getVariable("ACTOR", "fieldName")` to look up attributes of the currently authenticated actor. This enables ownership-based filtering and user-scoped entity creation without passing the current user as an explicit parameter.

## Structure

- Expression: `TypeName!getVariable("ACTOR", "claimField")`
- Common uses:
  - **Ownership lookup in operations**: `User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()` to find the current user entity
  - **Derived access filtering**: `Entity!filter(e | e.owner.email == String!getVariable("ACTOR", "email"))` to restrict access to owned records
  - **Default values**: `Email!getVariable("ACTOR", "email")` as a default for audit fields
  - **Session-level role checks**: `Boolean!getVariable('ACTOR', 'isActiveAdmin')` to check current user's role
- The actor must have a matching claim defined (e.g., `email::EMAIL` claim)
- Works with the actor's principal transfer object fields

## Examples

### itracker
`createInitiative` operation uses `User!filter(u | u.email == itracker::types::String!getVariable("ACTOR", "email"))!any()` to find the current user and assign ownership. `UserActor.initiatives` access uses the same pattern in its derived getter to show users only their own initiatives (plus role-based visibility for finance users).

### SkillMatrix
`admin::User.actorIsAdmin` uses `SkillMatrix::types::Boolean!getVariable('ACTOR', 'isActiveAdmin')` to check whether the currently logged-in user is an admin. This derived attribute is then used with `enabledBy` to conditionally enable admin-only UI controls (e.g., toggling admin/HR flags, deleting users).

### Alba
Extensively used for authorization: `Product.userOwnsProduct = self.author.email == Alba::types::String!getVariable("ACTOR", "email")` checks product ownership. `Task.isAssigneeCurrentUser` compares task assignee to current actor. `Product.author` default expression uses `User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()` to auto-assign current user as author on creation. Actor access points filter data by current user identity.

### Viterra Demo
Partner actor access points use `viterra::types::String!getVariable("ACTOR", "email")` for row-level security: `openReports` filters `Report!filter(r | r.client.email == String!getVariable("ACTOR", "email"))` to show only the partner's own reports. Same pattern for `closedReports` and `partnerData` access points. Email is the actor claim type, mapped from `ClientTransfer.email`.

### KozutEugyfelClient
Operations use `e_ugyfelszolgalat::types::String!getVariable("USER", "email")` to resolve the current user in the `elolvas` (mark-as-read) operation: `Felhasznalo!filter(f | f.email == String!getVariable("USER", "email"))!any()`. Permission derived attributes also use it: `self.felelos.email == String!getVariable("USER", "email")` for authorization checks. Notable: uses `"USER"` as the variable scope name instead of the more common `"ACTOR"`.

### judo-demo-miniworkflow
Pervasive use across all workflow operations and permission attributes. Every operation resolves the current user: `User!filter(u | u.email == MiniWorkflow::types::Email!getVariable('ACTOR', 'email'))!any()`. Permission derived attributes on Document compare `self.owner` with the resolved current user to determine ownership-based permissions (`isAcceptable`, `isClosable`, `isReviewable`, `isRejectable`). Access points (`myDocuments`, `waitingForApproval`) also use the ACTOR variable for filtering.

### InterfaceRegister
The Dashboard access point uses `User!filter(u | u.email == InterfaceRegister::types::String!getVariable("ACTOR", "email"))!any()` to resolve the current user and present their personalized dashboard with `welcomeText = 'Hi, ' + self.firstName`. The actor claim is defined as EMAIL type on the EnterpriseArchitect actor, following the standard email-based identity resolution pattern.

### judo-partner
Actor defines a claim `Partner::partner::Actor::email::EMAIL` for email-based identity resolution. The Actor is managed and anonymous-capable, with `Partner::partner::User` as the principal transfer object. The `partnerList` access uses `self` getter to resolve the current user's dashboard, implicitly leveraging the actor context for user-scoped data.

### KozutEugyfelModelTest
Three KOZUT-realm actors (UgyfelszolgalatiMunkatars, SzervezetiEgysegMunkatars, SzervezetiEgysegVezeto) each define an EMAIL claim mapped to `Felhasznalo.email`. The claim enables principal resolution for the `intezendoBejelentesek` DERIVED access that uses `self.intezendok` to navigate from the authenticated user to their assigned complaints.

### workflow-poc
Pervasive ACTOR variable usage for workflow authorization. `Token.isAssigneeLogged = self.assignee!isDefined() and self.assignee.email == String!getVariable("ACTOR", "email")` checks if current user is the assignee. `Token.isSupervisorLogged` checks supervisor role membership via `self.state.supervisor.users!filter(u | u.email == String!getVariable("ACTOR", "email"))!count() > 0`. The `checkout` operation resolves current user for self-assignment. Actor access `taskList` uses `User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()`.

## Trade-offs

- Pros: Automatic user context, no explicit parameter passing, works in both operations and access expressions
- Cons: Relies on actor claim configuration, limited to claim-exposed fields, requires understanding of the ACTOR variable scope
- Prefer when: Operations or access expressions need the current user identity for ownership or filtering

## Related Patterns

- [derived-access-filtering](derived-access-filtering.md)
- [default-value-patterns](default-value-patterns.md)

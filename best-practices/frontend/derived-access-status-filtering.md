---
id: "derived-access-status-filtering"
title: "Derived Access Points for Status-Based Filtered Views"
domain: "frontend"
category: "mapping"
score: 19.6
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - doors-model
---
## Description

Use multiple DERIVED access points on an actor, each with a `getterExpression` filter, to create separate menu items that show filtered views of the same underlying entity based on its lifecycle status. Instead of a single table page with runtime filter controls, each status-based subset gets its own navigation entry. This creates a task-oriented menu where users can directly navigate to "Created Contracts", "Pending Contracts", "Rejected Contracts", etc. without manually applying filters. The generated frontend produces distinct table pages per access point, all backed by the same transfer object and table definition.

## Structure

ESM model pattern:
```xml
<!-- Multiple access points on the same entity, filtered by status -->
<access name="createdInitiatives" accessType="DERIVED"
        getterExpression="self.initiatives!filter(i | i.status == DocumentStatus#CREATED)">
  <target type="Contract" />
</access>

<access name="inProgressInitiatives" accessType="DERIVED"
        getterExpression="self.initiatives!filter(i | i.status == DocumentStatus#PENDING)">
  <target type="Contract" />
</access>

<access name="rejectedInitiatives" accessType="DERIVED"
        getterExpression="self.initiatives!filter(i | i.status == DocumentStatus#REJECTED)">
  <target type="Contract" />
</access>

<!-- Each access point maps to its own menu item -->
<menuItem name="createdInitiativesMenu" label="Letrehozott" access="createdInitiatives" />
<menuItem name="inProgressInitiativesMenu" label="Feltoltott" access="inProgressInitiatives" />
<menuItem name="rejectedInitiativesMenu" label="Elutasitottak" access="rejectedInitiatives" />
```

Generated frontend structure:
```
pages/
  CreatedInitiatives/AccessTablePage/   # Shows only CREATED contracts
  InProgressInitiatives/AccessTablePage/ # Shows only PENDING contracts
  RejectedInitiatives/AccessTablePage/   # Shows only REJECTED contracts
  ClosedInitiatives/AccessTablePage/     # Shows only CLOSED contracts
```

All share the same `Contracts` table definition and `Contract` transfer object.

## Examples

### doors-model
Employee actor defines 19 access points, of which 12+ are DERIVED with status-based filters on the Contract entity. The navigation menu organizes these into groups: "My Tasks" (approval, signing, closing), "My Contracts as Officer" (created, uploaded, rejected, finalized, to close, in progress), "Contracts" (database, valid, in progress global/division), and "Partners" (4 partner types). A single `Contracts` table definition with 8 columns (sequence, creationDate, registrationNumber, title, status, officerName, contractorName, partnerName) is reused across all filtered views.

## Trade-offs

- **Pros**: Task-oriented navigation with zero frontend code; pre-filtered views reduce cognitive load; each view can have distinct permissions (read-only vs. editable); backend handles filtering efficiently via getter expressions
- **Cons**: Many menu items can overwhelm the navigation; each filtered view is a separate generated page (code duplication); adding a new status requires a new access point and menu item; no ability to combine status filters at runtime
- **When to use**: Workflow-driven applications where entities progress through lifecycle states and users need quick access to entities in specific states

## Related Patterns

- [approval-workflow-conditional-visibility](approval-workflow-conditional-visibility.md)
- [dual-actor-frontend-architecture](dual-actor-frontend-architecture.md)
- [admin-default-generated-ui](admin-default-generated-ui.md)

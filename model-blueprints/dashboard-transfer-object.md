---
id: "dashboard-transfer-object"
title: "Dashboard Transfer Object with Statistics"
score: 62.7
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - InterfaceRegister
---
## Description

A dashboard transfer object that serves as the main access point for an actor, aggregating multiple entity collections via relations and providing summary attributes or operations for common actions. The dashboard TO maps to a user entity and provides a personalized landing page view. In full implementations, it aggregates multiple entity collections via relations and provides a statistics sub-object with computed counts. In minimal implementations, it provides a derived welcome text and operations for creating key domain entities. The dashboard is accessed as a 0..1 access point on the actor type.

## Detection Query

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%Dashboard%" } }) {
  items { fqn name
    relations { items { name lower upper } totalCount }
    operations { items { name } totalCount }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{ACTOR_NAME}}Dashboard"
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "Statistics"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Statistics", name: "totalUsers"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Statistics", name: "activeUsers"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Statistics", name: "activeOrganizations"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **AdminDashboard**: `MLSZKSZPlatform::services::admin::AdminDashboard`
  - Attributes: isLeadership
  - Relations (14): cities, capabilities, offer, request, news, userInvitationRequestTO, companyUser, organizations, invitation, registrationRequest, announcements, statistics, auditLog, configuration
  - Operations (7): createCity, createCapability, createAnnouncement (custom), createOrganization (custom), syncFeed (custom), inviteBulk (custom), exportAuditLog (custom)
- **Statistics TO**: `MLSZKSZPlatform::services::admin::Statistics`
  - 16 count attributes: totalUsers, activeUsers, activeOrganizations, pendingOrganizations, pendingUsers, totalNews, totalOffers, totalRequests, totalAnnouncements, totalContent, hiddenUsers, visibleUsers, recentNews, recentOffers, recentRequests, recentAnnouncements
  - Relation: organizationStatistics (0..* to OrganizationStatistic)
- **OrganizationStatistic TO**: name, totalUsers, activeUsers, hiddenUsers, visibleUsers

### InterfaceRegister
- **Dashboard**: `InterfaceRegister::enterpriseArchitect::Dashboard` [maps User]
  - Attributes: welcomeText (DERIVED) -- personalized greeting computed from the logged-in user
  - Operations (3): createApplication (MAPPED), createHighLevelConnection (MAPPED), createUser (MAPPED)
  - No relations or statistics sub-object -- this is a minimal dashboard variant
- The Dashboard maps to the User entity, with operations delegating to User.createApplication, User.createHighLevelConnection, and User.createUser
- Each create operation takes an unmapped input TO (CreateApplicationInput, CreateHighLevelConnectionInput, CreateUserInput) and produces a mapped output TO
- Accessed by the EnterpriseArchitect actor as `dashboard [0..1]` (non-CRUD)
- This is the simplest dashboard variant: a derived welcome text plus factory operations, with no collection relations or statistics aggregation

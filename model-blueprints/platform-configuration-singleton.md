---
id: "platform-configuration-singleton"
title: "Platform Configuration Singleton Entity"
score: 70.7
usage_count: 3
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - rackinspect
  - park-here
---
## Description

A singleton Configuration entity that stores platform-wide settings. It is updateable but not createable or deleteable (exactly one instance exists, seeded at initialization). Typical attributes include email sender address (senderEmail), base URL, platform name, and various configurable parameters like expiry durations (invitationExpiryDays, verificationExpiryMinutes). It also holds email templates as text fields (invitationEmailTemplate, verificationEmailTemplate, approvalEmailTemplate). The configuration is exposed via a transfer object with an updateConfiguration operation. Some variants store document templates as binary fields and business-specific settings (margin percentages, closing times). Other variants are fully non-CRUD (all flags false) where updates go through custom operations or are admin-managed.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Configuration%" } }) {
  items { fqn name createable updateable deleteable
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Configuration",
  createable: false, updateable: true, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Configuration", name: "senderEmail"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Configuration", name: "baseUrl"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Configuration", name: "platformName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Configuration", name: "{{EXPIRY_PARAM_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Configuration", name: "{{TEMPLATE_NAME}}"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::Configuration`
  - createable=false, updateable=true, deleteable=false
  - Attributes: senderEmail (req), baseUrl (req), platformName (req), invitationExpiryDays (req), verificationExpiryMinutes (req), invitationEmailTemplate, verificationEmailTemplate, approvalEmailTemplate, postPublishedEmailTemplate
- **Transfer Object**: `MLSZKSZPlatform::services::admin::AdminConfigurationTO`
  - Mapped to Configuration entity
  - Operation: updateConfiguration (custom implementation)
- **Input TO**: `MLSZKSZPlatform::services::admin::ConfigurationInput` (all fields optional for partial updates)
- Accessed from AdminDashboard via `configuration` relation (0..1)

### rackinspect
- **Entity**: `rackinspect::entities::Configuration` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes (12): senderEmail (req), emailTemplate (req), closingTime (req), incidentNotificationEmail (req), netMarginPercent (req, default: 40), updateExchangeRates (req, default: true), assessmentSheetTemplate (req), reviewReportTemplate (req), offerTemplate (req), completionCertificateTemplate (req), workReportTemplate (req), jobSheetTemplate (req)
  - Relations: minimumOfferPrices (0..* COMPOSITION to MinimumOfferPrice)
- Stores business parameters (margin, closing time) alongside email and document templates (binary)
- MinimumOfferPrice sub-entity holds per-currency minimum offer thresholds

### park-here
- **Entity**: `ParkHere::entities::Configuration` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes (6): senderEmail (req), contactEmail (req), doormanEmailTemplate (req), deletationEmailTemplate (req), modificationEmailTemplate (req), reminderEmailTemplate (req)
  - Relations: doormans (0..* ASSOC to Doorman), additionalDays (0..* ASSOC to AdditionalDay)
- Focused on email configuration: stores the sender address, a contact email, and four email templates for different notification scenarios (doorman alerts, deletion notices, modification notices, reminders)
- **Transfer Objects**: `ParkHere::services::ConfigurationSettings` (mapped, with isConfigurationExist flag) exposes configuration/createDoorman/createDay operations; `ParkHere::services::ConfigurationInput` (unmapped input with all template fields)
- Also manages doorman assignments and calendar day overrides (work days/holidays) via associated entities

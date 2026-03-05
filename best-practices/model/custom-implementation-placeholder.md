---
id: "custom-implementation-placeholder"
title: "Custom Implementation Placeholder Operations"
domain: "model"
category: "operation"
score: 162.3
usage_count: 10
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - rackinspect
  - skillmatrix-frontend
  - alba
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
  - judo-partner
  - kozut-eugyfel-model-test
  - workflow-poc
---
## Description

Operations that require complex business logic beyond JQL capabilities are defined in the model with empty or comment-only bodies (`// no code`, `// no op`, `// sdk`). These serve as placeholders that declare the operation signature (input, output, faults) in the model while deferring implementation to custom backend Java code.

## Structure

- Operation is defined on entity or transfer with full signature (input type, output type, fault type)
- Body contains only a comment: `// no code` or `// no op` or `// sdk`
- Backend Java implementation is provided in a custom OSGi component
- The `.generator-ignore` file typically includes the custom implementation files

Common scenarios requiring custom implementation:
- Complex scoring/evaluation logic
- External system integration (JSON parsing, email)
- Multi-step business workflows
- Authentication/activation flows
- Document generation (PDF templates, Excel export)
- Status transition workflows with side effects

## Examples

### Trivia
Six operations use placeholders: `Test.submit` (scoring logic), `Test.exclude` (admin exclusion), `admin::Question.upload/download` (JSON import/export), `player::Application.register` (user registration), and `player::Application.activate` (code-based activation).

### RackInspect
`.generator-ignore` reveals 12+ custom implementations including: `GenerateJobTask`, `GenerateWorkReport`, `GenerateCompletionCertificate`, `GenerateAssessmentSheetPreview`, `GenerateReviewReportPreview`, `StatusToDone/InProgress/WontFix/WontStart` (job sheet item status transitions), `GetRackOperation`, `GetElementFaultOperation`.

### SkillMatrix
`report::Result.createExcel` is a custom implementation placeholder for Excel report generation (noted as "implemented by Robi"). `admin::User.createTestData` is a STATIC custom implementation for generating test data. Both operations define their signature in the model but defer logic to backend code.

### Alba
8 custom-implementation operations: `Product.approveVersion()`, `Product.finalize()`, `Product.revokeApproval()`, `Product.assignApproval()` (workflow state transitions with event creation), `User.finalizeProfile()` (profile validation and activation), `Task.closeTask()` (task completion with product state effects), plus static `createProduct` and `finalizeAccount` on service transfers. All have empty bodies requiring backend Java implementation.

### MLSZKSZPlatform
10 custom operations covering workflow, integration, and admin functions: `Initializer.init` (data seeding), `AdminDashboard.createAnnouncement/createOrganization/syncFeed/inviteBulk/exportAuditLog` (complex admin workflows), `AdminConfigurationTO.updateConfiguration` (platform settings), `FeedPanel.requestPost` (feed interaction), `RegistrationTransfer.registration/validate/verifyUserInvitation/lookupPostalCode` (multi-step registration with email verification). The `.generator-ignore` lists 44 `*CustomImplementation.java.default` files, showing extensive custom backend work.

### ParkHere
All 20+ operations use `customImplementation=true` with `// sdk` or empty body comments. Key operations include: `favoriteCar`, `deleteCar` (car management), `reservation`, `modificateReservation`, `deleteReservation`, `cancelReservation` (reservation lifecycle), `holiday`, `deleteHoliday`, `queryReservationsForHoliday` (holiday management), `configuration`, `createDoorman`, `createDay` (admin configuration). All use `BusinessError` fault type for consistent error handling.

### IndamediaAdTrack
All 17 operations use `customImplementation=true` for external platform API integration. Operations span 4 domains: client management (`createClient`, `updateClient`, `newAccount`, `createAggregatedCampaign`), campaign tracking (`updateCampaign`, `syncData`, `syncCosts`, `syncCostByDate`, `untrack`), account management (`setGoogleCredential`, `testConnection`, `fetchAvailableCampaigns`, `updateAccount`), and aggregated campaigns (`createTrackedCampaign`, `updateAggregatedCampaign`, `syncData`, `deleteAggregatedCampaign`). All use `BusinessError` fault type.

### judo-partner
Multiple operations require custom implementations for external system integration and complex logic: `Partner.queryTaxpayer` (NAV tax authority API integration), `Partner.validate`/`Partner.validateTaxNumber` (tax number validation logic), `NAVConfig.clearCache` (API cache management), `Taxpayer.updatePartner`/`TaxpayerAddress.addToPartner` (staging-to-domain data transformation), `Import.validateAll`/`Import.migrateAll` (bulk partner import orchestration), `Country.importCountries`/`Import.partnerImport` (JSON bulk import parsing).

### KozutEugyfelModelTest
Three custom operations for external integration: `JarokeloBejelentes.szinkronizal()` (static, synchronizes from external pavement system), `Esemeny.emailKuldes(EmailKuldesInput)` (single-recipient email sending), `Esemeny.emailKuldesTobbCimzett(EmailKuldesTobbCimzettInput)` (multi-recipient email sending). All are static operations with `customImplementation=true`.

### workflow-poc
Several operations use placeholder bodies for custom or deferred implementation: `Token.trigger` (`// TODO` body, workflow event processing), `Context.createContext` (`// NOOP` body, context creation), `Workflow.upload` (`// Java` body, YAML parsing and workflow definition validation with `DeclarationError` fault). The `Action.run` base operation has `// NOOP` body, with concrete subtypes providing actual implementations.

## Trade-offs

- Pros: Model declares the full API contract, generated code provides scaffolding, custom logic is isolated
- Cons: Disconnect between model and implementation, empty bodies may be missed during review
- Prefer when: Business logic is too complex for JQL expressions or requires external integrations

## Related Patterns

- [singleton-entity](singleton-entity.md)

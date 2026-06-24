---
id: "custom-operation-osgi-component"
title: "Custom Operation OSGi Component Registration"
domain: "backend"
category: "di"
score: 80.8
usage_count: 14
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - alba
  - mlszksz-platform
  - viterra_demo
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - doors-model
---
## Description

The standard pattern for registering custom operation implementations as OSGi Declarative Services components. Each custom operation class implements a generated interface from the SDK module and is registered via `@Component(immediate = true, service = ...)`. Dependencies (DAOs, external services) are injected via `@Reference` field annotations.

## Structure

```java
// Value-returning operation
@Component(immediate = true, service = DeleteVariant.class)   // service = the generated interface
public class DeleteVariantCustomImplementation implements DeleteVariant {

    @Reference
    LanguageVariantDao languageVariantDao;

    @Override
    public LanguageVariant apply(LanguageVariant _this) throws BusinessErrorException {
        // value-returning ops use apply(...)
        return languageVariantDao.update(_this);
    }
}

// Void operation
@Component(immediate = true, service = DeleteTemplate.class)
public class DeleteTemplateCustomImplementation implements DeleteTemplate {

    @Reference
    TemplateDao templateDao;

    @Override
    public void accept(Template _this) throws BusinessErrorException {
        // void ops use accept(...)
        templateDao.delete(_this);
    }
}
```

Key elements:
- `immediate = true` ensures the component starts when the bundle activates
- `service = X.class` MUST reference the generated interface class exactly; not a supertype, not `Object.class`
- The generated interface name is **`OperationName`** only — e.g. `DeleteVariant`, `RenameTemplate`, `CreateTemplate`. NOT `EntityNameOperationNameOperation`.
- Void-returning ops implement `accept(...)`; value-returning ops implement `apply(...)`. The method name `execute` does not exist on generated interfaces.
- `_this` is the entity instance the operation is called on (first parameter for INSTANCE ops); absent for STATIC ops.
- `@Reference` injects DAO and service dependencies from the OSGi service registry
- Generated interfaces live under `application/app/src/main/java/.../operation/compsychletter/<path>/` (or wherever the `judo-psm-generator-sdk-core-empty-custom-operation-osgi` plugin writes them for this project).

## Examples

### Trivia
8 custom operations registered as OSGi components (e.g., `RegisterCustomImplementation`, `EnterCustomImplementation`). Each implements a generated interface like `hu.blackbelt.trivia.operation.trivia.actors.player.application.Register` and injects DAOs such as `UserDao`, `ContestDao`, `EmailService`.

### RackInspect
~120 custom operations across 7 domain areas. Operations split into entity-level (toggles, init, permissions) under `_default_transferobjecttypes/entities/` and service-level (fault registry, offers, items) under `services/`. Most delegate to shared services: `@Reference OfferService offerService;` then `offerService.closeOffer(_this);`.

### itracker
11 `.java.default` scaffolds generated but none customized. All remain as unimplemented stubs (throwing `UnsupportedOperationException`). Model scripts via `script2operation.jar` handle all business logic instead. Demonstrates the OSGi component structure is generated and ready for customization when needed.

### ALBA
9 custom operations across product lifecycle (CreateProduct, Finalize, ApproveVersion, RevokeApproval, DraftNewVersion, AssignApproval), user profile (FinalizeProfile), and task management (CloseTask). Injections include 10+ DAOs and `VariableResolver` for actor resolution. Service-level operations under `services/authorproduct/` and `services/adminproduct/`.

### mlszksz-platform
65+ custom operations across 4 service domains (admin, companyadmin, feed, registration). All follow the same `@Component(immediate = true, service = Interface.class)` pattern. Operations inject shared business services (PostService, AuditLogService, ActorService) rather than DAOs directly, exemplifying a clean service-delegation approach at scale.

### viterra_demo
7 `.java.default` stubs demonstrating the generated scaffold pattern. Operations span entity-level (`_default_transferobjecttypes/report/`) and transfer-object-level (`reporttransfer/`, `partneropenreporttransfer/`). Each stub shows the full OSGi wiring: `@Component(immediate = true, service = Accept.class)` with Javadoc instructions for renaming, implementing, and adding to `.generator-ignore`.

### judo-demo-miniworkflow
10 `.java.default` scaffolds across entity-level (`_default_transferobjecttypes/document/`, `user/`) and transfer-object-level (`documenttransfer/`). Each uses `@Component(immediate = true, service = X.class)` with FQN references. Javadoc contains model script logic as implementation hints. Demonstrates the standard JUDO scaffold with usage instructions (rename, implement, add to `.generator-ignore`).

### Ubives
42 custom operations across 10 service domains (account, application, dashboardorganization, invitation, invitelink, organization, organizationaccount, partnerdashboard, profile, user). All inject shared services (OrganizationService, ApplicationService, InviteService, AccessService, UserService) via `@Reference` and delegate with one-line calls. Two init operations under `_default_transferobjecttypes/entities/initializer/`.

### ParkHere
20 custom operations across 11 service contexts (car, carsettings, configurationsettings, holiday, holidaypanel, profilesettings, reservationspanel, userforinput, userreservation, userreservationpanel, usersettings). All inject shared services (ReservationService, CarService, HolidayService, ActorService, EmailSenderService) via `@Reference` and delegate business logic. Init operation under `_default_transferobjecttypes/entities/initializer/`.

### Indamedia-AdTrack
17 custom operations across 5 transfer domains (accounttransfer, aggregatedcampaigntransfer, clientpanel, clienttransfer, trackedcampaigntransfer). All inject shared services (`AccountService`, `TrackedCampaignService`, `AggregatedCampaignService`, `ClientService`) via `@Reference` and delegate with one-line calls. Example: `FetchAvailableCampaignsCustomImplementation` injects `AccountService` and calls `accountService.syncAvailableCampaings(_this)`.

### InterfaceRegister
10 `.java.default` stubs across 3 contexts: 4 initializer operations (InitBrands, InitBusinessDataTypes, InitUsers, InitVendors), 3 user-context operations (CreateUser, CreateApplication, CreateHighLevelConnection), and 3 dashboard-context operations (same 3 operations). All remain as unimplemented scaffolds with `@Component(immediate = true, service = OperationInterface.class)` wiring, using FQN references and standard Javadoc usage instructions.

### judo-partner
15 custom operations across partner management domains: unbound operations (CreatePartner, PartnerImport, ImportCountries), bound partner operations (Delete, Validate, QueryTaxpayer), bound import operations (ValidateAll, MigrateAll, Validate, Migrate), bound address/contact operations (SetAsPrimary), and NAV config (ClearCache). All delegate to 7 service classes (PartnerServices, TaxpayerServices, ImportPartnerServices, etc.) via `@Reference`.

### workflow-poc
4 custom operations plus 2 utility services registered as OSGi components. Operations: `CreateContextCustomImplementation`, `TriggerCustomImplementation`, `UploadCustomImplementation`, `RunCustomImplementation`. Utility services `WorkflowUtils` and `DiagramUtils` are registered as `@Component(immediate = true, service = WorkflowUtils.class)` and injected into operations via `@Reference`. Operations inject 5-10 DAOs each plus utility services and `FileStoreService`.

### doors-model
11 custom operations declared in the ESM model with `customImplementation="true"` but implemented in a separate `doors-backend` repository (not present). Operations span: `generateDocument`, `validate`, `uploadFile`, `uploadSignedContract`, `customContractSave`, `customContractGet`, `createContract`, `init` (ContractType), `loadNavData`, `generateRandomContracts`, `generateRandomPartners`. Demonstrates the model-only project pattern where the model declares the operation contract and the backend project provides the OSGi component implementations in package `hu.blackbelt.doors.operations`.

## Trade-offs

- Pros: Standard OSGi pattern, supports hot-reload in Karaf, clear separation of generated and custom code
- Cons: Requires OSGi container, cannot easily unit test without OSGi or a DI bridge pattern
- Alternative: Delegation pattern where OSGi component delegates to POJO (see agent-docs)

## Anti-Patterns

- **Wrong method name (`execute`)** — The generated `@FunctionalInterface` declares `accept` (void) or `apply` (value-returning). Implementing `execute(...)` instead compiles because `@Override` on a non-existent interface method is a compile error — it will be caught immediately. Using `execute` without `@Override` compiles but the OSGi service is never called (the generated call site calls `accept`/`apply`).
- **Wrong interface name pattern** — The generator emits class name `OperationName` (e.g. `DeleteVariant`), not `EntityNameOperationNameOperation` (e.g. `LanguageVariantDeleteVariantOperation`). Using the wrong name causes `ClassNotFoundException` or `cannot be resolved to a type` at compile time.
- **Omitting `throws BusinessErrorException` on `apply`/`accept`** — The generated interface declares the checked exception; implementations must also declare it or the class will not compile when implementing the interface.

## Related Patterns

- dual-dao-pattern
- entity-re-fetch-pattern
- service-delegation-pattern
- script-driven-operations

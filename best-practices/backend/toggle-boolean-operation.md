---
id: "toggle-boolean-operation"
title: "Toggle Boolean Flag Operation Pattern"
domain: "backend"
category: "operation"
score: 64.3
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - mlszksz-platform
  - ubives
---
## Description

A highly reusable custom operation pattern for toggling boolean flags on entities. Each toggle operation follows an identical structure: (1) re-fetch entity by identifier, (2) flip the boolean field, (3) update with mask, (4) optionally trigger parent validation. This pattern appears 24+ times across 16 entity types in RackInspect, making it one of the most common custom operation patterns in JUDO projects.

## Structure

```java
@Component(immediate = true, service = ToggleActive.class)
public class ToggleActiveCustomImplementation implements ToggleActive {
    @Reference EntityDao dao;
    @Reference Validate validate;  // Optional: parent validation

    @Override
    public void accept(Entity _this) {
        Entity entity = dao.getById(_this.identifier()).orElseThrow();
        entity.setActive(!entity.getActive());
        dao.update(entity, EntityMask.entityMask());
        // Optional: cascade validation to parent
        Parent parent = dao.queryContainer(entity, ParentMask.parentMask()).orElseThrow();
        validate.accept(parent);
    }
}
```

Common toggle variants: `ToggleActive`, `TogglePrimary`, `ToggleBilling`, `ToggleHeadquarters`, `TogglePostal`, `ToggleDelivery`, `ToggleEszamla`, `TogglePrimaryContact`, `ToggleStandaloneStorable`.

## Examples

### RackInspect
24 toggle implementations across Address (5: Active/Billing/Delivery/Headquarters/Postal), BankAccount (2: Active/Primary), CompanyAddress (5), CompanyEmail (2), EmailAddress (3: Active/Eszamla/PrimaryContact), Partner (1), PhoneNumber (2), Unit (2: Active/StandaloneStorable), User (1), UserAddress/Email/Phone (2 each). Most trigger `validate.accept(partner)` after toggle.

### mlszksz-platform
2 `ActivateToggleCustomImplementation` classes for City and Capability master data entities. Both delegate to `MasterDataService.toggleCityActive()` / `toggleCapabilityActive()`, following the service delegation pattern. Used by platform admins to enable/disable master data entries without deletion.

### Ubives
6 Enable/Disable operation pairs: `EnableOrganizationRegistration`/`DisableOrganizationRegistration` (sets `isRegistrationFeatureSupported` flag), `EnableUser`/`DisableUser` (sets user `enabled` flag), `EnableAccess`/`DisableAccess` (sets access `enabled` flag). Each delegates to a service method (e.g., `organizationService.enableRegistration(id)`). Same operations repeated across multiple actor views (dashboardorganization, organization, partnerdashboard).

## Trade-offs

- Pros: Extremely uniform and predictable, easy to generate, minimal code per operation
- Cons: Each toggle is a separate class (could be generalized), mask with no fields causes full update
- Alternative: Single generic toggle service parameterized by entity type and field name

## Related Patterns

- entity-re-fetch-pattern
- mutable-entity-update-pattern
- mask-field-projection

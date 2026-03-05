---
id: "relation-based-entity-creation"
title: "Relation-Based Child Entity Creation"
domain: "backend"
category: "data-access"
score: 80.0
usage_count: 5
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - ubives
  - park-here
  - judo-partner
  - workflow-poc
---
## Description

Creating child entities through a parent entity's DAO relation method rather than directly via the child DAO. The parent DAO provides `createChildEntities(parent, childForCreate)` methods that automatically establish the parent-child relationship. This is used when the child entity is a containment relation of the parent.

## Structure

```java
// Create child through parent relation
parentDao.createChildEntities(parentEntity, ChildForCreate.builder()
    .withField1(value1)
    .withField2(value2)
    .build());
```

The parent DAO also provides query methods for navigating relations:
```java
List<Child> children = parentDao.queryChildren(parent).selectList();
Child child = parentDao.queryChild(parent);  // single-valued
```

## Examples

### Trivia
`testDao.createPrompts(test, PromptForCreate.builder().withNumber(i + 1).withQuestion(questions.get(i)).build())` -- creates numbered Prompt entities as children of a Test entity in a loop during contest entry.

### Ubives
`organizationEntityDao.createApplications(org, ApplicationEntityForCreate.builder().withName(name).withApplicationToken(apiKey).build())` creates applications within an organization. `organizationEntityDao.createUsers(org, List.of(userForCreate))` creates users within an organization. `organizationEntityDao.createInvitations(org, invitationForCreate)` creates invitations as organization children.

### ParkHere
`userDao.createCars(user, CarForCreate.builder().withLicensePlate().withManufacturer().withModel().withIsFavorite().build())` creates cars as children of a user. `userDao.createHolidays(user, HolidayForCreate.builder().withStartDate().withEndDate().build())` creates holidays. `configurationDao.createDoormans(configuration, List.of(doormanForCreate))` creates doormen with garage assignments. `configurationDao.createAdditionalDays(configuration, additionalDayForCreate)` creates additional calendar days.

### judo-partner
`partnerDao.createAddresses(partner, AddressForCreate.builder().withCountry(country).withCity(city).withZip(zip).withLine1(line1).withIsPrimary(true).build())` creates addresses as children of a partner. `partnerDao.createContacts(partner, ContactForCreate.builder().withName(name).withEmail(email).withIsPrimary(true).build())` creates contacts. `importDao.createPartners(imprt, ImportPartnerForCreate.builder()...build())` creates import partner records.

### workflow-poc
Extensive use for workflow structure creation: `workflowVersionDao.createEvents(workflowVersion, EventTypeForCreate.builder().withEventID(eventID).withLabel(label).build())` creates events as children of a version. `workflowVersionDao.createStates(workflowVersion, StateForCreate.builder().withName(name).build())` creates states. `stateDao.createTransitions(state, TransitionForCreate.builder().withRole(role).withEvent(event).build())` creates transitions. `contextDao.createLogs(context, LogEntryForCreate.builder()...build())` creates log entries.

## Trade-offs

- Pros: Automatically establishes parent-child relationship, type-safe, cleaner than setting foreign key manually
- Cons: Requires the parent entity to be persisted first, child must be a modeled containment relation
- Alternative: Create child directly via child DAO and set parent relation in the builder

## Related Patterns

- builder-pattern-entity-creation
- dao-fluent-query-filter

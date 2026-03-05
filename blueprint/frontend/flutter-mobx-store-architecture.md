---
id: "flutter-mobx-store-architecture"
title: "MobX Store Architecture for Flutter Frontend"
domain: "frontend"
category: "state"
score: 61.8
usage_count: 4
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
  - ams-frontend
alternatives:
  - viewmodel-context-pattern
---
## Description

The JUDO Flutter frontend uses MobX for reactive state management across three layers: (1) Data stores -- one per transfer object entity with `@observable` fields and `@action` setters, (2) Page stores -- per-page MobX stores holding repository references, `PageState`, `LoadingState` per action, error messages, sort/filter/pagination state, and CRUD action methods, (3) NavigationState -- a singleton MobX store managing breadcrumb stack, current page title, and page actions. All UI rendering uses `Observer` widgets for automatic reactivity.

## Structure

```dart
// Data store (per entity)
class UserStore extends _UserStore with _$UserStore {
  @observable String? email;
  @observable String? firstName;
  @observable bool? isActiveAdmin;
  @action void setEmail(String? val) => email = val;
  // identity: internal__identifier, internal__signedIdentifier
  // permissions: internal__updatable, internal__deletable
  void updateWith(UserStore other) { /* bulk update */ }
  UserStore clone() { /* deep copy */ }
}

// Page store (per page)
class UsersTablePageStore {
  final Repository _repo;
  final PageState pageState;
  LoadingState refreshActionLoadingState;
  @observable String? errorMessage;
  @action Future<void> getUsers({int? queryLimit, bool? isNext}) async { ... }
}
```

## Examples

### SkillMatrix
52 data stores across 3 actors (Admin: 2, HR Employee: 20, Professional: 30). Each page has its own PageStore with action-specific LoadingState objects that disable all buttons during async operations. NavigationState (lazySingleton via get_it) maintains breadcrumb stack with push/pop semantics for drill-down navigation.

### kozut-eugyfel-client
~90 data stores across 3 actors (Munkatars: ~50, Admin: ~35, E-Ugyfel: ~5). Page stores implement advanced filtering via `selectableFilters` list and `availableFilterList` observable, cursor-based pagination with `nextPageCounter`, and `@computed` getters for `nextButtonEnable`/`previousButtonEnable`.

### kozut-eugyfel-model-test
Model defines 16+ entity types generating data stores with clone() and updateWith() methods used in the clone-edit-save workflow. Stores include bejelentes, felhasznalo, megye, esemeny, ertesites, megjegyzes, tovabbitas, resztvevo, kep, and lezaras.

### ams-frontend
Two actors with stores including `ActorsAdminCampaignStore` (8 attributes + 2 relations), `ActorsManagerRequestStore` (10 attributes including enum types), and `ActorsManagerManagerApprovalListStore` (with `approvals` relation). Enum stores: `EntitiesCampaignStatus` (OPEN/CLOSED), `EntitiesStatus` (PENDING/APPROVED/REJECTED), `EntitiesRequestType` (ACCESS/REVOKE/CONFIRMATION).

## Trade-offs

- **Pros**: Fine-grained reactivity; generated stores have consistent patterns; Observable fields auto-update UI; LoadingState prevents double-clicks
- **Cons**: Large number of generated stores; MobX code generation adds build step; no equivalent of Pandino hook override for behavior customization
- **When to use**: Standard pattern for all JUDO Flutter frontends -- automatically generated

## Related Patterns

- [flutter-frontend-framework](flutter-frontend-framework.md)
- [viewmodel-context-pattern](viewmodel-context-pattern.md)
- [flutter-clone-edit-save-pattern](flutter-clone-edit-save-pattern.md)

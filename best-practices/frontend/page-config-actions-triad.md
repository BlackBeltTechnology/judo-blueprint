---
id: "page-config-actions-triad"
title: "Page-Config-Actions Triad Pattern (Flutter)"
domain: "frontend"
category: "page"
score: 52.3
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
  - ams-frontend
---
## Description

Every generated JUDO Flutter page consists of three coordinated files forming a "triad": (1) `page.dart` -- the MobX page store with observable state, computed properties, and action methods for data fetching; (2) `page__config.dart` -- table configuration (filters, sorting, column specs, row click behavior); (3) `page_actions.dart` -- user interaction handlers (refresh, add, navigate). The page widget instantiates all three and passes them to the responsive layout bodies. Additionally, each page may include `sort_comparator.dart` for custom sort logic and responsive layout files in `mobile/`, `tablet/`, and `desktop/` directories.

## Structure

```
{entity}/{page_type}/
  page.dart              # MobX PageStore with @observable, @computed, @action
  page__config.dart      # TableConfig with filters, sorting, defaults
  page__config__typedefs.dart  # Type definitions for config
  page_actions.dart      # Button handlers, navigation actions
  sort_comparator.dart   # Custom sorting logic
  package.dart           # Part directives grouping all files
  mobile/body.dart       # Mobile layout (4-column)
  tablet/body.dart       # Tablet layout (8-column)
  desktop/body.dart      # Desktop layout (12-column)
  dialogs/               # Optional dialog definitions
```

```dart
// page.dart - State management
abstract class _ExampleTablePageStore with Store {
  @observable ObservableList<EntityStore> items;
  @observable int nextPageCounter = 0;
  @computed bool get nextButtonEnable => items.length == queryLimit;
  @action Future<void> loadData() async { ... }
}

// page__config.dart - Configuration
class ExampleTablePageConfig {
  final TableConfig tableConfig = TableConfig(
    rowClickNavigate: true,
    selectableFilters: [...],
    sortColumnName: 'name',
  );
}

// page_actions.dart - Interactions
class ExampleTablePageActions {
  void onRefresh() => pageStore.loadData();
  void onAdd() => navigation.navigateTo(Routes.createPage);
}
```

## Examples

### kozut-eugyfel-client
~120 pages across 3 actors, each following the triad pattern. The Bejelentes (Report) entity alone has 25+ page variations. Table pages define `selectableFilters` with 5 filter types (string, dateTime, numeric, boolean, enum). Page stores use `SchedulerBinding.instance.addPostFrameCallback` to set navigation title and page actions after build. All files are grouped via Dart `part` directives in `package.dart`.

### kozut-eugyfel-model-test
Model defines page structure generating the triad for all 7 page types: dashboard, table, view, create, update, operation_input, and operation_output. Admin actor generates 58 routes, Munkatars 52 routes, each as a page-config-actions triad with 3 responsive layouts.

### ams-frontend
Campaigns View page demonstrates the triad with `page__config.dart` defining default sort for two embedded tables (Confirmation Requests sorted by applicationName, Applications sorted by identifier). The `page_actions.dart` includes Open/Close/Load campaign operations with conditional enablement via `targetStore.isOpen`/`isClosed`/`isEmpty` observables and confirmation dialogs.

## Trade-offs

- **Pros**: Clear separation of state, configuration, and interaction; consistent pattern across all pages; easy to locate specific customization points; generated automatically
- **Cons**: High file count per page (7+ files including layouts); tight coupling between triad files; all three must be modified together for changes
- **When to use**: Standard JUDO Flutter pattern -- automatically generated for all pages

## Related Patterns

- [three-layout-responsive-pattern](three-layout-responsive-pattern.md)
- [flutter-mobx-store-architecture](flutter-mobx-store-architecture.md)
- [flutter-frontend-framework](flutter-frontend-framework.md)

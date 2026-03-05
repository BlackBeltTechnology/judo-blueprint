---
id: "flutter-clone-edit-save-pattern"
title: "Flutter Clone-Edit-Save Pattern for Entity Updates"
domain: "frontend"
category: "form"
score: 36.5
usage_count: 2
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - kozut-eugyfel-model-test
  - ams-frontend
alternatives:
  - view-edit-mode-toggle
---
## Description

In JUDO Flutter frontends, editing an entity follows a clone-navigate-save workflow rather than an in-place toggle. The view page clones the MobX data store, navigates to a separate update page with the cloned copy, allows the user to edit fields, and on save copies the clone back to the original store before persisting via API. This differs from the React pattern where view and edit happen on the same page with a boolean `editMode` toggle. The clone approach prevents partial edits from corrupting the displayed data if the user cancels.

## Structure

```dart
// In page_actions.dart (view page)
void onEdit() {
  var clonedStore = targetStore.clone();
  navigation.open(Routes.updatePage, arguments: clonedStore);
}

// In update page on save
void onSave() async {
  targetStore.updateWith(clonedStore);
  await repository.update(targetStore);
  navigation.close();
}

// In data store
EntityStore clone() { /* deep copy all @observable fields */ }
void updateWith(EntityStore other) { /* bulk field copy */ }
```

Separate page types: view (read-only) and update (editable) are generated as distinct pages with their own layouts and actions, rather than sharing a single page with mode toggling.

## Examples

### kozut-eugyfel-model-test
Admin actor Bejelentesek (Reports) view page has Edit action that clones the store and navigates to the update page. All ~120 pages across 3 actors follow this pattern with dedicated view/update page pairs generated from the model.

### ams-frontend
Applications and Campaigns entities both have separate view and update pages. Application View offers Edit action (navigates to update page) and Delete. Campaign View includes Edit plus 3 bound operations (Open, Close, Load). The clone-edit-save pattern ensures campaign data stays intact if the user cancels mid-edit.

## Trade-offs

- **Pros**: No partial edit corruption on cancel; clear separation of concerns; undo is trivial (discard clone); each page type has focused responsibility
- **Cons**: Double the page count (view + update); navigation overhead for simple edits; more generated files per entity
- **When to prefer view-edit-mode-toggle**: In React frontends where the generated pattern uses in-place editing with `editMode` boolean

## Related Patterns

- [view-edit-mode-toggle](view-edit-mode-toggle.md)
- [flutter-mobx-store-architecture](flutter-mobx-store-architecture.md)
- [page-config-actions-triad](page-config-actions-triad.md)

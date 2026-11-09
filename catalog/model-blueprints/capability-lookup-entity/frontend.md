## Frontend guidance

Capabilities appear in three places: as tags on cards, as a filter on lists, and as a field on the administrator's forms. Hook keys in the frontend are generated per page or per container, so the names below are examples of the pattern, not fixed identifiers.

### Filter with type-ahead

A list filter lets a user pick capabilities by typing. The filter hook loads the active capabilities and filters the options, using the list's own data source. Hide inactive capabilities here.

```tsx
export function useCapabilityOptions(capabilities: Capability[]) {
  return capabilities.filter((c) => c.isActive);
}
```

The hook is project code. Register it for the page that shows the filter, using the key the framework generates for that page.

### Show tags on cards

Cards show each capability as a chip. Show the existing tags even when a capability is inactive, so the record still reads correctly.

### Pre-fill the update form

The update dialog for a capability loads the current name and description before the user edits them. Use the framework's template action hook for that dialog, and register it under the key the framework generates for the dialog's page and container.

### Toggle as a switch

Show isActive as a switch in the administrator's table. The switch calls the toggle operation and refreshes the row.

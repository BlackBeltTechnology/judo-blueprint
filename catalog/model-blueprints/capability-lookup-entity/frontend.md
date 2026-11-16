## Frontend guidance

Capabilities appear in three places: as tags on cards, as a filter on lists, and as a field on the administrator's forms. Hook keys in the frontend are generated per page or per container, so the names below are examples of the pattern, not fixed identifiers.

### Filter with type-ahead

A list filter lets a user pick capabilities by typing. A container action hook can supply typeahead or `filter<Field>Options` handlers that narrow the options. Hide inactive capabilities here. The handler names must match the action definition type generated for the container (see `customization.ts` and `types.ts` there).

```tsx
export function useCapabilityOptions(capabilities: Capability[]) {
  return capabilities.filter((c) => c.isActive);
}
```

The hook is application code. Register it through the generated scaffold `register<Container>ActionsHook(context)` (copy the `.default` file) with `context.registerService(<CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY, hook)`. Scaffolds exist only when the matching hook flag is set in the model.

### Show tags on cards

Cards show each capability as a chip. Show the existing tags even when a capability is inactive, so the record still reads correctly.

### Pre-fill the update form

The update dialog for a capability loads the current name and description before the user edits them. Use the container action hook of that dialog, if the generated container type offers a template handler, and register it through the generated scaffold. The dialog's operation is the platform's getTemplate behaviour, which returns a prepopulated prototype.

### Toggle as a switch

Show isActive as a switch in the administrator's table. The switch calls the toggle operation and refreshes the row.

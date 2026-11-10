## Frontend guidance

The lookup needs no custom frontend in most projects. The generated pages and the generated selector for the association are enough.

- **Selector.** A 0..1 or 1..1 association renders as a single selector. A 0..* association renders as a table with attach and detach (the association's update flag controls those buttons). See the [ESM to UI mappings](../../agent-docs/frontend/esm-to-ui-mappings/README.md).
- **Administrator list.** Keep the generated table and form if the administrator's access has create and update rights. Otherwise the table is view-only (filter and refresh only).
- **Hide retired options.** The generated selector lists every row. To offer only active entries, restrict the choices in the model with a range on the association, or filter in a hook. A hook is project code and is registered under the key the framework generates for the page.
- **Name-only views.** For partners and end users, the name-only transfer object keeps the flag out of their forms.

Framework in all source projects: React.

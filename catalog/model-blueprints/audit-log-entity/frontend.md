## Frontend guidance

### Keep the generated read-only pages, hide the form

Creating the entity generates its View, Form and Table pages. Because rows come only from the backend, hide the generated Form page. Keep the View and Table pages, read-only, for the admin dashboard.

### Replace the details section with a custom element

The generated detail view shows the raw attributes. A custom visual element can replace that section with a readable view: one colored chip per action type, the parsed details as labeled key-value pairs, and a copy button for the entity id. Build the chip colors from the enumeration values so new values need no code change to be shown.

- Parse the details JSON and fall back to the raw text when parsing fails.
- Translate the labels through the project's i18n keys, not hard-coded text.

### Add an export button to the table toolbar

A container hook can add an export button to the audit table toolbar. The button opens a dialog with a date picker for the start date, then calls the export operation and downloads the returned file.

## Examples

### mlszksz-platform

- Framework: React.
- The detail section and the toolbar button are registered in the project's custom implementation hooks.
- Action-type colors cover all 32 enumeration values.

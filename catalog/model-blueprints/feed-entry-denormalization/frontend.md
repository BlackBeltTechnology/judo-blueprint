## Frontend guidance

### Replace the generated table with a feed component

The generated list of feed rows is a table. For a feed, replace it with a custom component that loads the rows in pages and renders each row as a card. The card shows the type through a colour cue, the capabilities as chips, the organization name as a link, the validity dates where they apply, and a short summary.

### Load pages by seek, not by offset

A list call without an explicit seek returns all rows, so pagination is opt-in. Load the rows with seek pagination, ordered by creation time, newest first. Load the next page when the user reaches the end of the list (infinite scroll). This keeps the page fast as the feed grows.

### Keep filters on the page

Provide filters for the capabilities (with autocomplete) and for the entry type. Hide the filter bar while the user scrolls down, and show it again on scroll up, so the list has room.

### Navigate by type

A row carries the content id and the entry type. The row's open action is overridden through a page action hook (a registered service that replaces the generated action). It queries the derived relation for that type, and then opens the matching detail page. Do not open the detail page from the row id alone.

### Show a create action only to the right roles

A floating action button to request a new post appears only for users with the matching organization role. Check the role on the client and enforce it on the server.

## Examples

### Variant seen in practice

- The feed container replaces the generated table, with infinite scroll and seek pagination ordered by creation time.
- Each feed card has a colour cue by post type, capability chips, and a clickable organization name.
- A page action hook overrides the open action, so each type navigates to its own detail page.
- The request-post button is shown only to the company admin and reader roles.
- The application's own component and hook names are application code. Copy the pattern, not the names.

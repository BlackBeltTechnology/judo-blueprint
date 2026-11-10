## Frontend guidance

Each actor gets its own generated pages from its transfer objects. A restricted actor sees a smaller set of pages than the admin.

- Keep the list and view pages of the restricted projection. Hide the create and edit pages where the projection is read-only.
- Read-only fields (MAPPED from a read-only binding, DERIVED) show as locked or plain text. Do not add an edit control for them.
- Hook keys are generated per page and per container. Do not write a hook key by hand; find it in the generated page for that container.
- Admin-only fields exist only in the admin projection. Do not expose them through the restricted pages.

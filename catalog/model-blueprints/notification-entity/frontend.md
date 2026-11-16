## Frontend guidance

Notification pages can stay generated or be replaced by a custom inbox.

- Keep the generated Table and View pages for Notification if a plain list is enough. They are read-only.
- For a card inbox, the list must be exposed by the model as a custom implementation element. Register a component for the per-element key generated in the page's `customization.ts` (scaffold: `register<Container>CustomImplementations.tsx.default`) and keep the generated View page for detail.
- Map the NotificationType values to icons in the UI. Keep the map complete, so every type has an icon.
- When a user taps a notification, follow the reference id to the content. Do not store the content in the notification.
- Hook keys are generated per page and per container. Do not write a hook key by hand; find it in the generated page for that container.

## Frontend guidance

The open and close actions are generated on the View page. Keep them there and show the one that applies.

- Show the open action only when the status is CLOSED, and the close action only when it is OPEN. A derived boolean such as isOpen or isClosed on the transfer object is referenced by the operation's `hiddenBy` or `enabledBy`.
- Show the current state as text or a badge. Use the enumeration value, not a boolean.
- With the three CRUD flags false the generated UI has no create, edit or delete controls. The state changes only through the operations.
- Hook keys are generated per page and per container. Do not write a hook key by hand; find it in the generated page for that container.

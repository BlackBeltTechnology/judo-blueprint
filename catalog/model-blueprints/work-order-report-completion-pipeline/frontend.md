## Generated pages to keep

- The offer view with its work order table: keep. Users open the work orders from the offer.
- The work order view with its item table and its report table: keep. The items are grouped by finding in the table, sorted by finding and then by number.
- The work report view with its kind and status: keep. Show the kind as a read-only label after creation.
- Attachments and documents: keep as a list on the item and the report. A user uploads a photo to the item, not to the work order.

## Hide or disable actions by their guard

- Hide the `generateWorkOrder` action when `workOrderGenerationAllowed` is false. Show it while the offer is accepted and no completion certificate exists.
- Hide the report's `toDone` action when the report has no document (kind WORK_REPORT) or no signed document (kind COMPLETION_CERTIFICATE). *verify* the completion rule, see the entry's Constraints section.
- Hide the item's `toDone` action until the item has at least one attachment, and show a hint that a photo is needed.
- For `toWontFix`, open a form with one required text field for the reason. Send the reason as the operation input. Do not set the status first and ask for the reason afterwards.

A hidden action does not protect the operation. The backend check in the operation stays, and it returns the same business error the hidden action would have prevented.

## Status display

Show the `WorkStatus` as a coloured label with four states: not started, in progress, done and won't fix. Use the same labels in the item, the report and the work order.

## Hooks

- Use a custom hook for the `generateWorkOrder` action only when the guard needs data beyond the offer's own fields.
- Use a dialog hook for `toWontFix` to validate that the reason is not blank before the request is sent.
- Keep the generated action forms for `toDone`. Their only extra rule is the visibility guard above.

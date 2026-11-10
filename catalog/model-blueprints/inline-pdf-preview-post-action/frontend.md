## Frontend guidance

### Register the hook for the dialog that starts the operation

Write a dialog form action hook for the input dialog of the document operation. Use the hook key the framework generates for that page and container. Do not copy a key from another page.

```tsx
// Shape of the callback, generic names. The generated hook interface gives the exact types.
const postOperationAction = async (output, onSubmit, onClose) => {
  if (!output.file) {
    await onClose();
    return;
  }
  await onClose();
  const fileToken = typeof output.file === 'string' ? output.file : output.file.id ?? output.file;
  try {
    await openInline(fileToken);
  } catch (error) {
    console.error('Could not open the document', error);
  }
};
```

### Close the dialog before opening the file

Call the close callback first. Then open the file. This keeps the dialog from staying open behind the PDF tab.

### Open the file in inline mode

The generated `fileHandling.downloadFile` helper requests the file with the token (`X-Token` header) and a disposition. Pass `inline` to render it instead of saving it; `attachment` saves it. Per the platform docs an inline download renders in a dialog frame; rackinspect (project practice) opens it in a new browser tab, so check what your generated version does.

### Handle both token shapes

An operation may return the token as a string, or as an object that holds the identifier. Accept both, as the example above does.

### Keep the fallback

If the output has no file, close the dialog and stop. Do not show an error for a successful operation that produced nothing to open.

## Examples

### rackinspect

- Two dialog hooks implement this pattern: one for an assessment sheet preview, one for a review report preview. Each closes its input dialog, then opens the PDF inline in a new browser tab.
- Both hooks accept the file as a string token or an object with an identifier.

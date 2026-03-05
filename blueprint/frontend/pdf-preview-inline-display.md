---
id: "pdf-preview-inline-display"
title: "Inline PDF Preview via downloadFile with Inline Mode"
domain: "frontend"
category: "component"
score: 10.8
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
---
## Description

After a backend operation generates a PDF document, intercept the operation output in a dialog action hook, extract the file token, and display the PDF inline in the browser using the JUDO `downloadFile` utility with `'inline'` mode. This avoids showing a separate output dialog or forcing a file download. Requires adding `@react-pdf-viewer/core`, `@react-pdf-viewer/page-navigation`, and `pdfjs-dist` as extra npm dependencies via a generator override fragment.

## Structure

```typescript
// Dialog action hook
const hookImpl = () => ({
  async postGeneratePreviewAction(output, _onSubmit, onClose) {
    if (output && output.file) {
      await onClose(); // Close input dialog first
      const fileToken = typeof output.file === 'string'
        ? output.file
        : output.file.id || output.file;
      await downloadFile({ file: fileToken }, 'file', 'inline');
    } else {
      await onClose();
    }
  },
});

// Extra dependencies (generator-overrides/ui-react/actor/package.json.dependencies.extra.fragment.hbs)
// "@react-pdf-viewer/core": "^3.12.0",
// "@react-pdf-viewer/page-navigation": "^3.12.0",
// "pdfjs-dist": "3.11.174",
```

## Examples

### RackInspect
Two dialog hooks implement PDF preview: assessment sheet preview and review report preview. Both intercept the `postGenerate*PreviewAction`, close the input dialog, extract the file token from the operation output, and call `downloadFile` with `'inline'` mode. The review report hook also sets default dates (closedDate=now, expireDate=created+1month) via `postGetTemplateAction`.

## Trade-offs

- **Pros**: Seamless PDF viewing experience; no separate download step; user stays in the application flow
- **Cons**: Requires extra npm dependencies; browser PDF rendering varies; file token extraction logic can be fragile
- **When to use**: When backend operations generate PDF reports that users need to preview before finalizing

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [generator-override-extra-dependencies](generator-override-extra-dependencies.md)

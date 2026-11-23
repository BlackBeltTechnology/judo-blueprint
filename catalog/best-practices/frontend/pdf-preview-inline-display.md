---
id: pdf-preview-inline-display
title: Inline PDF Preview via downloadFile with Inline Mode
description: "After a backend operation generates a PDF, use the dialog's post-operation action hook to take the file token from the operation output and open it with the generated downloadFile helper in inline mode instead of saving it."
aliases: [inline PDF preview, PDF preview after operation]
keywords: [inline, pdf, preview, downloadfile, disposition, file token, post operation hook, dialog hook, react-pdf-viewer]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "project:park-here", "status:emerging"]
category: component
status: emerging
projects: [rackinspect, park-here]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/dialogs/registerServicesFault_registry_servicesFaultRegistryFaultRegistry_View_EditGenerateAssessmentSheetPreviewInputFormActionsHook.tsx", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/dialogs/registerServicesFault_registry_servicesFaultRegistryFaultRegistry_View_EditGenerateReviewReportPreviewInputFormActionsHook.tsx"]
alternatives: []
related: [pandino-action-hook-override, generator-override-extra-dependencies]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Let users look at a generated PDF right after the operation that produced it, without a separate output dialog and without forcing a download.

## Practice

### Platform base

- The generated `fileHandling` helpers (`downloadFile`, `uploadFile`, `exportFile`, `extractFileNameFromToken`) wrap the two-phase token flow. `downloadFile` calls the download path with `?disposition=inline|attachment` and the token in the `X-Token` header; per the platform docs an inline download renders in a dialog frame ([custom attachments: token flow](../../agent-docs/frontend/advanced-patterns.md), [client side of the upload token flow](../../agent-docs/backend/platform-behavior-reference.md)).
- Page and dialog hook types have optional `post<Operation>Action` handlers whose parameters are generated for the page. Return the handler from the actions hook created from the generated `register<Page>ActionsHook` scaffold; check the generated types for the exact names ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)).

### Practice notes: preview in the post-operation hook

- In the post-operation handler of the input dialog, call the close callback first, then open the file with `downloadFile(..., 'inline')`. Closing first keeps the input dialog from staying open behind the PDF.
- Accept the token as a string or as an object holding the identifier; if the output has no file, only close the dialog and show no error.
- The `post<Operation>Action` name and signature below are illustrative; The example app opens the PDF in a new browser tab, so check what your generated version does for `inline`.
- The PDF viewer libraries (`@react-pdf-viewer/core`, `@react-pdf-viewer/page-navigation`, `pdfjs-dist`) are additions, put into the generated `package.json` through a generator override fragment ([[generator-override-extra-dependencies]]). That fragment list is not part of the platform docs' fragment table, which covers pom and Karaf files.

```typescript
// Illustrative handler shape; the generated hook type gives the real one.
async postGeneratePreviewAction(output, _onSubmit, onClose) {
  await onClose();
  if (output?.file) {
    const fileToken = typeof output.file === 'string' ? output.file : output.file.id ?? output.file;
    await downloadFile({ file: fileToken }, 'file', 'inline');
  }
}
```

## Rationale

The user stays in the application flow and sees the result at once. The cost is extra npm dependencies, browser-dependent PDF rendering and token extraction that depends on the operation output shape.

## Example

One app has several dialog hooks of this kind, each for a different generated document. Each closes the input dialog, takes the token from the operation output and calls `downloadFile` inline. One of them also sets default dates in `postGetTemplateAction`.

## When to avoid

- Users must keep the PDF as a file; use `attachment` mode.
- The PDF should show on an output page of the operation; model an output transfer object instead.

## Related

- [[pandino-action-hook-override]] — how action hooks are registered
- [[generator-override-extra-dependencies]] — adding the viewer npm packages

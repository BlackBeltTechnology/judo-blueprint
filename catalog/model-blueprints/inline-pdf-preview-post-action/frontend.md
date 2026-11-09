## Overview

Dialog form action hooks that intercept post-operation output from document generation operations and display the resulting PDF inline in the browser using `fileHandling().downloadFile()` with `'inline'` mode, bypassing the default output view dialog. Framework: React.

## Implementation Pattern

- **Hook type**: Dialog form action hooks (e.g., `*InputFormActionsHook`) registered via Pandino in `application-customizer.tsx`
- **Key callback**: `postOperationAction(output, onSubmit, onClose)` -- called after the backend operation returns successfully
- **Flow**: (1) Check if `output.file` exists, (2) call `await onClose()` to dismiss the input dialog, (3) extract the file token (handles both string JWT and object with `.id`), (4) call `downloadFile({ file: fileToken }, 'file', 'inline')` to open PDF in browser
- **File handling utility**: Uses `fileHandling()` from `~/utilities/file-handling` which resolves the file token to a download URL and opens it inline
- **Error handling**: Wraps the download call in try/catch with console.error fallback; closes the dialog even if no file is present
- **Naming convention**: The post-action callback follows the pattern `post<OperationName>Action` (e.g., `postGenerateAssessmentSheetPreviewForFaultRegistryAction`)

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesFault_registry_servicesFaultRegistryFaultRegistry_View_EditGenerateAssessmentSheetPreviewInputFormActionsHook.tsx`, `custom/hooks/dialogs/registerServicesFault_registry_servicesFaultRegistryFaultRegistry_View_EditGenerateReviewReportPreviewInputFormActionsHook.tsx`
- Pattern: Two dialog hooks implement the same pattern for different document types (assessment sheet preview and review report preview). Both close the input dialog first, then open the generated PDF inline in the browser tab.
- Notable: File token extraction handles both string JWT tokens and object wrappers (`typeof output.file === 'string' ? output.file : output.file.id || output.file`); the `'inline'` parameter to `downloadFile` triggers browser-native PDF viewer instead of a file download

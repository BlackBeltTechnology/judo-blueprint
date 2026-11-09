---
id: inline-pdf-preview-post-action
title: "Inline PDF Preview via Post-Operation Action Hook"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - rackinspect
---

## Description

A frontend-only pattern for displaying PDF documents inline in the browser after a server-side document generation operation completes, instead of showing the default generated output view dialog. A dialog form action hook provides a `postOperationAction` callback that receives the operation output (containing a file token/JWT), closes the input dialog, and uses the framework's `fileHandling().downloadFile()` utility with `'inline'` mode to open the PDF directly in the browser. This pattern is used for document preview workflows (e.g., assessment sheet preview, review report preview) where the user wants to see the generated PDF immediately without navigating to a separate output page. This is an implementation-only blueprint -- it customizes the default post-operation behavior for file-producing operations.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

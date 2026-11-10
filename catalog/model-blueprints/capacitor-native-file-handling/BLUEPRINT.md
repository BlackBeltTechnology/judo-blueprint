---
id: capacitor-native-file-handling
title: Capacitor Native File Download and Open
description: A file download override for Capacitor Android apps that saves the file to the device's download folder, notifies the user and opens the file on tap, while the web keeps the browser download.
aliases: [native download, native file open]
keywords: [capacitor, native, file, download, open, notification, filesystem]
tags: [domain:model, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: [inline-pdf-preview-post-action]
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Let a Capacitor Android user download a file and open it from the device, where a browser download would not leave a visible file. The web keeps the browser download unchanged.

### Native download saves and notifies

On native, the file is written to the download folder, a local notification names it, and a tap opens it. This gives the user a file they can find and open later.

### The override keeps the generated interface

The generated file utility is replaced by a project module with the same exports. Screens need no change, and only the save step differs by platform.

## Structure

The pattern is a frontend layer. A generator-ignore entry marks the generated file utility as overridden. A native file handler holds the save, notify and open steps, a blob-to-base64 helper, and a MIME map for common extensions. A re-export module lets custom views keep their import path. The native branch runs only when the app is on a native platform.

## Constraints

- Only the save step changes. The override keeps the generated utility's exports (`downloadFile`, `uploadFile`, `exportFile`, `extractFileNameFromToken`). `uploadFile` and the two-phase token flow (`~upload-token`, then multipart with `X-Token`) stay as generated; `downloadFile` calls the download path with `?disposition=inline|attachment` and `X-Token`.
- The native branch runs only on a native platform. The web download path must not change.
- The filesystem plugin writes base64 text. Convert binary data with an array buffer, not a string.
- On Android 10 and later, scoped storage needs no extra storage permission for the download folder.

## Variations

- **Share sheet instead of open.** Pass the file to the platform share sheet on tap, when the user should choose the app.
- **Inline preview kept separate.** A PDF preview in inline mode stays in the browser viewer; only downloads use the native save.
- **Web-only app.** Skip the override and keep the generated browser download.

## When to use

- A Capacitor Android app must give the user a saved, openable file after a download.
- Downloads are documents, spreadsheets or images that the user wants in the device's file list.

## When to avoid

- The app runs only in a browser. The generated download is enough.
- Files are previewed but never saved. Use an inline preview instead.
- The app needs a file picker or upload from the device. That is a separate capability.

## Related

- [[inline-pdf-preview-post-action]] — the inline preview that stays separate from the native save
- [[document-file-attachment]] — the binary document attribute whose files this pattern downloads
- [[capacitor-native-auth-pkce-passkey]] — the other Capacitor native concern in the same app

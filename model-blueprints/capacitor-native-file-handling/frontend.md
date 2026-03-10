## Overview

A platform-aware file handling override for JUDO React + Capacitor apps that routes file downloads through native filesystem and local notification APIs on Android, while using standard browser downloads on web. Framework: React (Capacitor Android).

## Implementation Pattern

The pattern overrides the generated `src/utilities/file-handling.tsx` via `.generator-ignore` and provides a custom implementation:

- **native-file-handler** (`custom/utilities/native-file-handler.ts`) -- Core native utilities:
  - `saveFile(blob, fileName)`: Converts blob to base64, writes to `Download/{fileName}` via `@capacitor/filesystem` (ExternalStorage directory, scoped storage on Android 10+)
  - `showDownloadNotification(fileName, fileUri, contentType)`: Schedules a local notification via `@capacitor/local-notifications`, with a listener that opens the file via `@capacitor-community/file-opener` when the notification is tapped
  - `blobToBase64(blob)`: ArrayBuffer-to-base64 conversion using `Uint8Array` + `btoa`
  - MIME type mapping for common file extensions (PDF, DOCX, XLSX, images, CSV, etc.)
- **custom-file-handling** (`custom/utilities/custom-file-handling.tsx`) -- Re-exports from the overridden `file-handling.tsx` so custom views that imported from this path continue to work.
- **StatusBarTheme** (`custom/utilities/status-bar-theme.ts`) -- Capacitor plugin registration for native status bar color control.

**Generator ignore**: `src/utilities/file-handling.tsx` is listed in `.generator-ignore`, meaning the generated file is replaced with a custom version that delegates to `native-file-handler.ts` when `Capacitor.isNativePlatform()` is true.

## Examples

### mlszksz-platform
- Framework: React (Capacitor Android)
- Key files: `custom/utilities/native-file-handler.ts`, `custom/utilities/custom-file-handling.tsx`, `.generator-ignore` (entry: `src/utilities/file-handling.tsx`)
- Pattern: Generator-ignore override of file-handling.tsx; native path uses Filesystem + LocalNotifications + FileOpener Capacitor plugins
- Notable: Scoped storage on Android 10+ (no permissions needed); local notification with tap-to-open file; base64 conversion for Capacitor Filesystem write

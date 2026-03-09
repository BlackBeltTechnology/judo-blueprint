---
id: capacitor-native-file-handling
title: "Capacitor Native File Download and Open"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A platform-aware file handling system that overrides the generated file download behavior for Capacitor native apps. On native platforms, downloaded files are saved to the device's Download folder via `@capacitor/filesystem`, a local notification is shown with the file name, and tapping the notification opens the file using `@capacitor-community/file-opener`. On web, the standard browser download behavior is used unchanged. The override is applied by listing `src/utilities/file-handling.tsx` in `.generator-ignore` and providing a custom implementation.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

---
id: push-notification-system
title: Push Notification System with Deep Linking and Badge
description: A frontend-only push notification system for Capacitor native apps that registers the device with the JUDO backend, shows foreground toasts, deep links notification taps to content and keeps an unread badge in sync.
aliases: [native push client, notification badge]
keywords: [push, notification, capacitor, fcm, deep link, badge, device registration, cold start]
tags: ["domain:frontend", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: none: frontend-only client code; the notification and device data live in the backend entries
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Let a native app receive push notifications from Firebase Cloud Messaging and act on them: register the device with the backend, show a toast while the app is open, open the right content page when the user taps a notification, and show an unread count. The client logic sits in custom React code on top of the generated frontend; the backend operations and entities it calls are described in the related entries.

### Registration is idempotent and retried

The client stores the registered token on the device and skips registration when it did not change. A failed registration or token update is kept and retried when the app resumes, with growing delays between attempts.

### A cold-start tap must not be lost

A tap that launches the app fires before login finishes and before the authenticated page tree exists. The client stores the tap on the device and replays it after login.

### One badge count, several views

The unread count lives in one small shared store, so the header bell and the bottom navigation always show the same value.

## Structure

The client is a set of cooperating modules registered through the application customizer: a header component with a bell and badge (registered as the single extra component of the app bar), a push hook that registers the device and handles notifications, a thin wrapper around the Capacitor push plugin, a badge store, a launch-notification store, a retry helper and a deep-link route added as an extra route. The backend side offers device register, deactivate and update-token operations and a notification list that the badge reads.

## Constraints

- The system is native-only. A web user reads the notification list page instead.
- The plugin listeners are registered before the registration call, so the first token event is not missed.
- Foreground notifications are shown only to an authenticated user.
- The unread badge count comes from the backend notification list, not from the push payload. The count request asks only for the total, not for rows.
- The backend decides who may see which notification; the client only hides and routes. See [[notification-entity]].
- Custom code lives in the gitignored `src/custom/` folder and survives regeneration. Hook registration happens in the application customizer, and extra routes in the extra routes file.

## Variations

- **Web push.** A service worker replaces the Capacitor plugin. The device registration, badge and deep-link parts stay the same.
- **Polling badge.** Without push, the bell polls the notification list. Use it when push is not available.
- **Type-aware deep link.** The link resolves the target to a type-specific page, as in [[post-generalization-hierarchy]]. A single target type needs no lookup.

## When to use

- A Capacitor-wrapped JUDO frontend needs push notifications with deep links.
- Device tokens are registered with the backend, which sends the push.

## When to avoid

- The app is web only; the in-app notification list is enough.
- The backend has no device registration; build that first, see [[firebase-push-notification-pipeline]].

## Related

- [[firebase-push-notification-pipeline]] — the backend delivery of the push messages this client receives
- [[notification-entity]] — the notification data the badge and list read
- [[capacitor-native-auth-pkce-passkey]] — native login that a cold-start tap must wait for
- [[post-generalization-hierarchy]] — the typed content the deep link opens in the example project

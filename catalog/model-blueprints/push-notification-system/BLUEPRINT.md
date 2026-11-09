---
id: push-notification-system
title: Push Notification System with Deep Linking and Badge
description: A complete push notification frontend system for Capacitor native apps that integrates Firebase Cloud Messaging (FCM) with the JUDO backend.
aliases: []
keywords: [push, notification, system, deep, linking, badge]
tags: ["domain:model", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-09
last_updated: 2026-03-09
format: legacy
---

## Description

A complete push notification frontend system for Capacitor native apps that integrates Firebase Cloud Messaging (FCM) with the JUDO backend. The system handles device registration/deactivation via backend API calls, displays foreground notifications as snackbar toasts, supports notification tap deep linking to specific content pages, maintains an unread badge count synced across header bell icon and bottom navigation, and captures cold-start notification taps that fire before the authenticated component tree is mounted. The system is native-only -- web users use the in-app notifications dashboard page. The pattern includes retry-with-backoff for device lifecycle API calls and Capacitor Preferences-based persistence for idempotent registration.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

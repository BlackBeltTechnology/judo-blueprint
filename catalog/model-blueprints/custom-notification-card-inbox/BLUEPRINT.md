---
id: custom-notification-card-inbox
title: Custom Notification Card Inbox Component
description: A custom notification list that replaces the generated notifications table with cards, each showing a type icon, a short message, a relative time and a delete action, and that opens the referenced entry when tapped.
aliases: [notification inbox, notification cards, notification list]
keywords: [notification, inbox, card, list, badge, pagination, deep link, custom component]
tags: ["domain:frontend", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-09
---
## Intent

Show a user's notifications as a readable list of cards instead of a dense data table, so that each item is easy to scan on a phone and tapping it goes straight to what it is about.

### Each card carries its meaning

A notification type has its own icon, so the user can tell an announcement from an approval at a glance. The message is clamped to a few lines, and the time is shown relative to now.

### The list keeps the header badge in step

Deleting a notification also lowers the unread count shown in the header, so the bell and the list never disagree.

## Structure

This is a frontend-only component. It has no model of its own: it displays the notification rows the backend already provides, and it does not add entities, attributes or relations.

Each row has a type, a message, a time, and an optional reference to a feed entry. The type decides the icon. The reference decides whether the card is tappable.

## Constraints

- The card is tappable only when the notification refers to an entry. A notification without a reference is shown but does not navigate.
- The delete action must not also trigger the card's tap action.
- The list loads more items on request rather than all at once.
- Relative times are formatted in the user's language.
- The header badge is decremented only after a delete succeeds.

## Variations

- **Read and unread states.** The card can show a read or unread marker. This needs a backend flag on the notification row.
- **Grouped by day.** Long lists can group cards under day headings instead of a single run.
- **Swipe to delete.** Delete can use a swipe gesture on touch devices, with the same confirmation rule as the button.

## When to use

- The generated table is hard to read on a phone and each row needs an icon or a tap target.
- Each notification links to another page, so tapping is the main action.
- The list is a feed the user scans rather than a set of records they compare.

## When to avoid

- The user needs to sort, filter or compare rows across many columns. Keep the generated table.
- The notifications are only counted, never read. A badge alone is enough.

## Related

- [[custom-post-detail-views]] — the post pages a notification card usually opens

---
id: custom-post-detail-views
title: Custom Post Detail View Components
description: A set of mobile-first, read-only custom views that replace the generated post detail layouts, with a shared wrapper that colors each post type and integrates contact actions and organization cards.
aliases: [post detail views, post view components, custom detail pages]
keywords: [post, detail, view, custom, container hook, mobile, read only, layout]
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

Give each post type a detail page that reads well on a phone and shows what the reader needs to act: who posted it, when, what it is about, and how to get in touch.

### One wrapper gives every post the same frame

All post views share one wrapper. It sets the padding, the card surface, and a left border in the post type's color, so a reader can tell the type from the page before reading it.

### Contact and organization are part of the view

The author's organization is shown as a compact card, and the e-mail and phone are offered as direct links. The reader does not need to go to another page to contact the poster.

## Structure

This is a frontend-only set of views. It has no model of its own: each view displays the data of an existing post or related entity, and it does not add entities, attributes or relations.

The views cover the four post types (news, offer, request and announcement), the organization detail page, and the profile page. Offers and requests add an interest action. Announcements are the simplest, with no organization card and no action.

## Constraints

- Views are read-only, except for the profile page, which saves its own fields.
- The shared wrapper sets the type color; a view does not choose its own color.
- Image downloads use the platform's binary access, not a plain link, so protected files load for signed-in users only.
- Contact links use the mail and phone schemes, so they open the device's own app.
- A view must still render when optional fields such as the image or the organization are missing.

## Variations

- **Read-only detail only.** A project that edits posts on a separate form can keep only the read-only views and leave the edit page generated.
- **Profile with instant save.** The profile page saves each field when it changes, after a short pause, instead of using an edit and save cycle. This suits a few simple fields.
- **Shared card and action helpers.** The organization card, contact actions and interest button are small shared components used by several views.

## When to use

- Post detail pages must read well on a phone and carry a clear type signal.
- Each post shows an author organization and contact details that the reader acts on.
- The generated detail layout is too dense for the content.

## When to avoid

- The generated layout already fits the content and the users. Replacing it adds upkeep for no gain.
- The page is an editing form with many fields. Keep the generated form.
- The views must match another platform's design exactly, and the custom styles would conflict.

## Related

- [[custom-notification-card-inbox]] — the notification list that opens these post pages

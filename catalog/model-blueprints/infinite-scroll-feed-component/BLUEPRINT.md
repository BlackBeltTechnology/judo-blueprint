---
id: infinite-scroll-feed-component
title: Infinite-Scroll Card-Based Feed Component
description: "A card-based feed component that replaces a generated data grid with an infinite-scrolling, mobile-first feed that uses cursor pagination and a filter drawer."
aliases: []
keywords: [infinite, scroll, card, based, feed, component]
tags: [domain:model, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: "none: frontend-only"
first_seen: 2026-03-09
last_updated: 2026-11-09
---
## Intent

Show a long list of feed entries as a scrolling feed of cards instead of a data grid table. The feed loads more entries as the reader reaches the end, and the reader narrows the list with filters that stay in place while scrolling.

### Cursor pagination, not offsets

Each page is requested after the last loaded item. A live feed then does not repeat or skip entries when new ones arrive, and the client needs no count query.

### Filters apply in batches

Filters are chosen in a drawer and applied together. The active filters persist for the session, so a reader who leaves the tab and returns sees the same list.

## Structure

The feed container orchestrates the filters, the pagination, the infinite scroll and the create action. It receives the fetch action, the page-open action and the owner from the generated page.

Each feed entry is a card. The card shows a colour-coded edge for the entry type, a meta row with type, organization and date, a short summary clamped to a few lines, validity dates for time-bound entries, capability tags and a sensitive-content badge. The organization name opens its organization.

The filter bar shows the active filters as chips. A drawer holds the editable filters: entry type (multi-select), title, summary, organization name, and capability (an autocomplete that searches the server).

The create action is a floating button that opens a bottom drawer. It is shown only to the roles allowed to create entries.

## Constraints

- Pages are requested with a cursor set to the last loaded item, asking for one more item than the page size. An extra item means another page exists.
- Entries are de-duplicated by identifier, because a live feed can return an entry twice across pages.
- The sentinel at the end of the list triggers the next page when it enters the viewport.
- Text filters use a contains match. The entry type filter uses an exact match.
- The capability autocomplete is debounced and queries the server.
- The create action is hidden for roles that may not create entries. The check happens in the interface, and the server must enforce the same rule.

## Variations

- **Offset pagination.** Use page numbers with a total count. This suits static lists where the count matters and the data does not change often.
- **Data grid.** Keep the generated table for desktop-first, dense lists. The card feed fits mobile reading better.
- **Filters on the page.** Show the filters inline instead of in a drawer. This suits wide screens but takes space on phones.

## When to use

- A long, changing list is read mostly on mobile.
- Readers scan entries in order and rarely need totals.
- Filters must narrow the list without leaving the scroll position.

## When to avoid

- The list is short and fixed.
- Readers need to sort or compare many columns at once.
- Exact page counts or jumps to a page number are required.

## Related

- [[feed-entry-denormalization]] — storing the fields a feed card needs on the entry itself
- [[custom-post-detail-views]] — the detail view opened from a feed card
- [[custom-statistics-dashboard]] — another custom frontend view on generated data

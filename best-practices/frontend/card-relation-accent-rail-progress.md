---
id: "card-relation-accent-rail-progress"
title: "Relation Card with Accent Rail and Live Progress Bar"
domain: "frontend"
category: "component"
score: 18.0
usage_count: 1
alternative_count: 0
first_seen: "2026-07-01"
last_updated: "2026-07-01"
projects:
  - park-here
---

## Description

Render a relation's `CardsContainer` rows as a custom card that leads with a slim brand-colored **left accent rail** and a single content column, instead of the default multi-field list. The card surfaces the record's day with an **inline localized weekday** (`Intl.DateTimeFormat(locale, { weekday: 'short' })`), presents key fields as compact icon rows, and replaces a vertical timeline with a **horizontal Start→Now→End progress bar** whose fill reflects elapsed time. When the record is *currently in progress* it gets a **live treatment** (pulsing rail, flowing fill, pulsing "now" marker + a small beacon/label) driven by `@mui/system` `keyframes`; upcoming records are static with a "starts in…" hint. All colors resolve from the theme palette so the card tracks the brand and adapts to light/dark. The card is wired via the generated `…ComponentConfigurationHook` `CardElement` slot, so no generated code is edited.

The "currently running" decision must be day-aware — see the Trade-offs note and the `agent-docs/frontend/advanced-patterns.md` "Date and Time Field Semantics" section: `Time` fields are deserialized onto today, so a same-calendar-day guard on the record's `Date` field is required.

## Structure

```
src/custom/hooks/components/
  UserActiveReservationsCard.tsx            # the card (accent rail, weekday, progress, live animation)
  activeReservationCard.logic.ts            # pure, DOM-free timing/formatting helpers (unit-tested)
  activeReservationCard.logic.test.ts       # vitest unit tests incl. the "another day" regression
  cards/…UserReservationsComponentConfigurationHook.tsx  # wires the card as CardElement
```

Pure logic (testable without a DOM):

```typescript
export function isSameCalendarDay(a: Date, b: Date): boolean {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}

export function computeReservationTimeline(
  reservationDate: Date, // Date type — the real day
  start: Date,           // Time type — pinned to today
  end: Date,             // Time type
  now?: Date | null,     // Time type (currentTime), pinned to today
): { state: 'upcoming' | 'running' | 'ended'; fraction: number; isToday: boolean } {
  if (now == null || !isSameCalendarDay(reservationDate, now)) {
    return { state: 'upcoming', fraction: 0, isToday: false };
  }
  const s = start.getTime(), e = end.getTime(), n = now.getTime();
  if (n < s) return { state: 'upcoming', fraction: 0, isToday: true };
  if (n > e) return { state: 'ended', fraction: 1, isToday: true };
  const span = e - s;
  return { state: 'running', fraction: span > 0 ? Math.min(1, Math.max(0, (n - s) / span)) : 0, isToday: true };
}
```

Live-treatment animations (only applied when `state === 'running'`):

```typescript
import { keyframes } from '@mui/system';
const railGlow = keyframes`0%,100% { box-shadow: 0 0 0 0 currentColor; } 50% { box-shadow: 2px 0 16px 0 currentColor; }`;
const flow = keyframes`0% { background-position: 0% 0; } 100% { background-position: 200% 0; }`;
const nowPulse = keyframes`0% { transform: scale(1); opacity: .6; } 100% { transform: scale(2.6); opacity: 0; }`;
```

Consistency details: a shared `CARD_RADIUS` is applied to both the `Card` and its action `Button`s so rounding matches; the weekday/date is the prominent header; theme `primary`/`secondary` drive the rail and "now" accents (no hardcoded hex).

## Examples

### park-here — UserActiveReservationsCard

Active reservations render as accent-rail cards. `date` is a `Date`; `startTime`/`endTime`/`currentTime` are `Time`. A reservation shows the pulsing "Running now" beacon + moving progress only when `isSameCalendarDay(date, currentTime)` and `startTime ≤ currentTime ≤ endTime`; a future-day reservation (whose time-of-day happens to be inside the window) stays static/upcoming. The guest branch swaps the car row for a reserver row (`reserverName (reserverCarId)`); Delete/Cancel/Edit visibility follows `isNotDeletable`/`isNotCancelable`.

## Trade-offs

- **Day-awareness is mandatory.** Because `Time` fields deserialize onto today, comparing them alone wrongly marks other-day records as "running". Always gate on the `Date` field via `isSameCalendarDay`. This is the single most important correctness detail of the pattern.
- **Extract pure logic.** Putting the timing/formatting in a framework-free module keeps it unit-testable with plain `vitest` (no `@testing-library`/`jsdom` needed) and lets you add a regression test for the cross-day case.
- **Animation cost.** The live treatment uses CSS `keyframes` (cheap, GPU-friendly) rather than JS timers; it only mounts for the running record, so a list of mostly-upcoming cards stays static.
- **Scope creep.** Redesign only the card that needs it (here, the active card) and leave sibling cards (e.g. previous reservations) untouched to keep the diff surgical.

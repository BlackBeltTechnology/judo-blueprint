---
id: auto-scrolling-scoreboard
title: Auto-Scrolling Scoreboard/Leaderboard Component
description: A kiosk-style leaderboard component with a medal podium and a self-scrolling list that pauses on touch and refreshes its data at the bottom, for public display screens.
aliases: [leaderboard component, kiosk scoreboard]
keywords: [scoreboard, leaderboard, auto scroll, refresh, pause, medal, kiosk, interval]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: component
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [glassmorphic-styled-components, complete-frontend-replacement, scoreboard-personal-best-pattern]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A scoreboard on an event or kiosk screen should run unattended: it scrolls through the entries by itself, lets a visitor stop it by touching, and reloads the data when it reaches the end.

## Practice

### Platform base

- The generated pages do not offer this display. It is a custom component, shown in a dialog or page that you register through the frontend hook mechanism ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md), [Pandino service registration](../../agent-docs/frontend/hooks/README.md)).
- The rows come from the generated service of the page or relation. The client requests the order: the model does not fix the sort order, so pass it in the query ([service generation](../../agent-docs/frontend/model-screen-layout.md)).
- Colors should come from the theme palette, which the actor's model colors and sub-themes drive ([theming](../../agent-docs/frontend/theming.md)).

### Project practice: podium plus self-scrolling list

This layer is project practice (trivia), not a platform feature:

- Split the rows: the top three as a podium with gold, silver and bronze avatars, the rest in a scrolling list.
- Scroll the list by a small step on a short timer. When the list reaches the bottom, request a data refresh after a cooldown.
- Touch or press pauses scrolling and release resumes it, which suits mobile and kiosk users.
- Highlight the current player's row in the theme's primary color.
- Always clear the interval when the component unmounts or pauses.

```tsx
// Example project code: not a platform component
useEffect(() => {
  const timer = setInterval(() => {
    if (!paused && listRef.current) {
      listRef.current.scrollTop += 1;
      if (atBottom(listRef.current)) refreshData();
    }
  }, 50);
  return () => clearInterval(timer);
}, [paused]);

<List onTouchStart={() => setPaused(true)} onTouchEnd={() => setPaused(false)}>
  {entries.map((entry) => (
    <ListItem key={entry.rank} sx={{ color: entry.isCurrentPlayer ? 'primary.main' : 'text.primary' }}>
      {/* rank, name, score, duration */}
    </ListItem>
  ))}
</List>
```

## Rationale

It suits public screens without any operator, and refreshing keeps the data current. The cost: a hand-written component, scroll behavior that differs between devices, and interval cleanup that is easy to get wrong.

## Example

trivia shows a dialog with the top three as colored medal avatars above an auto-scrolling list of the rest. The list moves one pixel every 50 ms, pauses on touch and refreshes every ten seconds through the generated list call of the personal-best relation, sorted by score descending, duration ascending, then finish time ascending. The current player is highlighted. The model side is in [[scoreboard-personal-best-pattern]].

## When to avoid

- The list is short enough to fit the screen.
- Users must read and interact with the rows; moving content hurts accessibility.
- A plain generated table with sorting is enough.

## Related

- [[scoreboard-personal-best-pattern]] — the model behind the ranked rows
- [[glassmorphic-styled-components]] — the visual style used around the dialog
- [[complete-frontend-replacement]] — the custom frontend that hosts it

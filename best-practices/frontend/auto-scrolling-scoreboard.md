---
id: "auto-scrolling-scoreboard"
title: "Auto-Scrolling Scoreboard/Leaderboard Component"
domain: "frontend"
category: "component"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

A TV/kiosk-style leaderboard component that auto-scrolls through entries, pauses on user interaction, and auto-refreshes data when reaching the bottom. Designed for public display or scoreboard screens. Typically features a top-3 medals section with special styling (gold/silver/bronze) and a scrolling follow-up list.

## Structure

```typescript
// Auto-scroll at 1px per 50ms
useEffect(() => {
  const interval = setInterval(() => {
    if (!isPaused && listRef.current) {
      listRef.current.scrollTop += 1;
      if (atBottom) {
        refreshData();  // Auto-refresh every 10s when at bottom
      }
    }
  }, 50);
  return () => clearInterval(interval);
}, [isPaused]);

// Touch/click to pause
<List onTouchStart={() => setPaused(true)} onTouchEnd={() => setPaused(false)}>
  {entries.map((entry, idx) => (
    <ListItem key={idx} sx={{
      color: entry.isCurrentPlayer ? 'primary.main' : 'text.primary'
    }}>
      {/* Rank, name, score, duration */}
    </ListItem>
  ))}
</List>
```

Top 3 use medal avatar colors: gold `#D4AF37`, silver `#B0B0B0`, bronze `#8C7853`.

## Examples

### Trivia
`ScoreboardDialog.tsx` renders Top 3 with colored avatar medals and a `Scoreboard` auto-scrolling component for follow-ups. Scrolls at 1px/50ms, pauses on touch, refreshes data every 10 seconds via `playerServiceForContestsImpl.listPersonalBests()` sorted by score desc, duration asc, timestamp asc. Current player highlighted in primary orange.

## Trade-offs

- **Pros**: Great for public displays and event screens; auto-refresh keeps data current; touch-to-pause is intuitive
- **Cons**: Custom implementation (not a library); scroll behavior may vary on different devices; requires careful interval cleanup
- **When to use**: Event/conference apps, game leaderboards, public display screens

## Related Patterns

- [glassmorphic-styled-components](glassmorphic-styled-components.md)
- [complete-frontend-replacement](complete-frontend-replacement.md)

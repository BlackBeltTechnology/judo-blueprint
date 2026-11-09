## Overview

The scoreboard/personal-best pattern manifests in the React frontend as a custom leaderboard dialog with a podium-style top-3 display and an auto-scrolling list for remaining players, highlighting the current player's entries across the ranking.

## Implementation Pattern

- **Two-tier ranking display**: The `ScoreboardDialog` splits `personalBests` into top-3 (displayed as an MUI `List` with medal-colored `Avatar` icons -- gold #D4AF37, silver #B0B0B0, bronze #8C7853) and remaining players (displayed in the `Scoreboard` scrolling component starting from position 4).
- **Auto-scrolling leaderboard**: The `Scoreboard` component in `CustomComponents.tsx` implements continuous auto-scrolling at 1px per 50ms interval. When the scroll reaches the bottom, it triggers a data refresh via `onRequestRefresh()` after a 10-second cooldown (`REFRESH_INTERVAL`). Touch events toggle scrolling on/off for mobile interaction.
- **Player highlighting**: The current player's name is highlighted in the primary theme color (`primary.main`) throughout both the top-3 list and the scrolling section, using a `currentPlayer` prop compared against each `item.playerName`.
- **Score ordering**: Data is fetched with `_orderBy` specifying score descending, duration ascending, and `timestampOfFinished` ascending -- rewarding higher scores first, then faster times, then earlier completion.
- **Duration formatting**: The `formatTime()` utility in `utils.ts` converts raw seconds into human-readable format (e.g., "2 m, 15s").
- **Data service integration**: The dialog calls `PlayerServiceForContestsImpl.listPersonalBests()` with the contest reference to fetch ranked results.

## Examples

### trivia
- Framework: React
- Key files: `src/trivia/ScoreboardDialog.tsx`, `src/trivia/CustomComponents.tsx` (Scoreboard component), `src/trivia/utils.ts`
- Pattern: Custom `ScoreboardDialog` fetches `personalBests` via `PlayerServiceForContestsImpl.listPersonalBests()` with multi-field ordering. Top-3 shown with medal-colored avatars; remaining players in an auto-scrolling `Scoreboard` list with periodic refresh.
- Notable: The auto-scroll implementation uses `setInterval` at 50ms with 1px increments and a 10-second refresh cooldown. The scoreboard is accessible both from the contest view ("Scoreboard" button) and from the results dialog after test submission.

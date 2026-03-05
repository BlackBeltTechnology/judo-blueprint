---
id: "localstorage-session-persistence"
title: "LocalStorage-Based Session Persistence"
domain: "frontend"
category: "state"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

Use `localStorage` to persist session state (user identity, current context, in-progress data) instead of OAuth/OIDC tokens or server-side sessions. This provides a lightweight authentication alternative for applications where full SSO is unnecessary, such as public-facing games or event kiosks. A "Reset" action simply clears localStorage and reloads the page.

## Structure

```typescript
// Initialize from localStorage
const [userId, setUserId] = useState(localStorage.getItem('app-user-id'));
const [contest, setContest] = useState(
  JSON.parse(localStorage.getItem('app-contest-id') || 'null')
);

// Persist on change
useEffect(() => {
  if (userId) localStorage.setItem('app-user-id', userId);
}, [userId]);

// Reset action
const handleReset = () => {
  localStorage.clear();
  window.location.reload();
};

// Authentication check
const isAuthenticated = typeof userId === 'string';
```

## Examples

### Trivia
Player frontend persists 8 keys: `trivia-user-id` (email), `trivia-nickname-id`, `trivia-user-code-id` (activation code), `trivia-contest-id` (JSON), `trivia-test-id`, `trivia-test-duration-id`, `trivia-prompt-list-id` (JSON), `trivia-answer-list-id` (JSON). Authentication is `typeof userId === 'string'`. "Reset" button in bottom nav clears all and reloads.

## Trade-offs

- **Pros**: No login screen friction; survives page refreshes; simple implementation; supports multi-user on same device via reset
- **Cons**: Not secure for sensitive data; limited to single browser; no cross-device sessions; no server-side session validation
- **When to use**: Public-facing apps, event kiosks, games, demos where full authentication is overkill

## Related Patterns

- [dialog-based-navigation](dialog-based-navigation.md)
- [error-code-mapping-pattern](error-code-mapping-pattern.md)

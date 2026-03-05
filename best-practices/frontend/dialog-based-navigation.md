---
id: "dialog-based-navigation"
title: "Dialog-Based Navigation with State Machine"
domain: "frontend"
category: "navigation"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

Replace React Router-based navigation with a state machine that controls which page/dialog is visible. Navigation is driven by a `PageType` state variable and boolean dialog-open flags rather than URL routes. This pattern is suited for single-page experiences like games, wizards, or kiosk-mode applications where URL-based routing adds no value.

## Structure

```typescript
// State machine type
type PageType = 'contests' | 'contest' | 'prompt' | 'scoreboard' | 'none';

// In App.tsx
const [activePage, setActivePage] = useState<PageType>('contests');
const [isRegistrationOpen, setRegistrationOpen] = useState(false);
const [isActivationOpen, setActivationOpen] = useState(false);
// ... more dialog states

return (
  <>
    {activePage === 'contests' && <Contests />}
    {activePage === 'contest' && <Contest />}
    <RegistrationDialog open={isRegistrationOpen} />
    <ActivationDialog open={isActivationOpen} />
    <BottomNavigation /> {/* Fixed nav for page switching */}
  </>
);
```

## Examples

### Trivia
Player frontend uses a 5-value `PageType` state machine (`contests`, `contest`, `prompt`, `scoreboard`, `none`) with 5 dialog-open boolean flags. Flow: Contests list -> Registration -> Activation -> Contest detail -> Quiz (PromptListDialog) -> Results -> Scoreboard. Bottom navigation bar provides "Contests" and "Reset" actions.

## Trade-offs

- **Pros**: No URL management overhead; clean state transitions; dialogs provide natural modal flow; works well for kiosk/embedded apps
- **Cons**: No deep linking; browser back button does not work; no URL-based state sharing; harder to test specific states
- **When to use**: Games, wizards, kiosk applications, or any UI where URL routing is unnecessary

## Related Patterns

- [complete-frontend-replacement](complete-frontend-replacement.md)
- [localstorage-session-persistence](localstorage-session-persistence.md)

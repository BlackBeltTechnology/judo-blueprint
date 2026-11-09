---
id: "breadcrumb-navigation-context"
title: "Breadcrumb Navigation Context with History Tracking"
domain: "frontend"
category: "navigation"
score: 34.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - actiongroup-test-react
---
## Description

Wrap React Router navigation in a custom `BreadcrumbProvider` context that tracks navigation history as a breadcrumb stack. The `useJudoNavigation()` hook provides `navigate()` (push to breadcrumb and go forward), `back()` (pop breadcrumb and go back), `clearNavigate()` (clear history and navigate), `isBackDisabled`, and `setTitle()`. This gives the application a consistent forward/back navigation model with visual breadcrumb rendering, independent of browser history.

## Structure

```typescript
// BreadcrumbProvider wraps routes
<BreadcrumbProvider>
  <Outlet />
</BreadcrumbProvider>

// Hook API
const { navigate, back, clearNavigate, isBackDisabled, setTitle } = useJudoNavigation();

// Forward navigation stores breadcrumb
navigate(`/galaxies/${row.__signedIdentifier}`);

// Back navigation pops breadcrumb
back();

// Clear navigation resets breadcrumb stack
clearNavigate('/galaxies');

// Visual breadcrumb component
<CustomBreadcrumb /> // Renders breadcrumb trail in header
```

## Examples

### ActionGroupTestReact
`BreadcrumbProvider` in `src/components/CustomBreadcrumb.tsx` maintains a breadcrumb history array. `navigate()` pushes current location + title. `back()` pops and navigates to previous. Header renders `CustomBreadcrumb` with max 2 visible items. Back button in Header uses `isBackDisabled` to disable when no history exists.

## Trade-offs

- **Pros**: Consistent back navigation independent of browser; visual breadcrumb trail; supports deep entity navigation chains (Galaxy > Star > Planet); title management per page
- **Cons**: Parallel to browser history (can get out of sync); breadcrumb state lost on page refresh; clearNavigate needed for sidebar navigation
- **When to use**: JUDO applications with deep entity navigation hierarchies where browser back button behavior is insufficient

## Related Patterns

- [dialog-based-navigation](dialog-based-navigation.md)
- [complete-frontend-replacement](complete-frontend-replacement.md)

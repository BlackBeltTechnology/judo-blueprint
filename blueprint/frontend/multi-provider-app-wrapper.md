---
id: "multi-provider-app-wrapper"
title: "Multi-Provider App Wrapper Pattern"
domain: "frontend"
category: "state"
score: 11.9
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
---
## Description

Compose the application root with a nested stack of React Context providers, each managing a specific cross-cutting concern: date localization, MUI theming, internationalization, toast notifications, dialog system, and navigation/breadcrumbs. The provider order matters -- inner providers can access outer provider values. This creates a clean dependency hierarchy where pages only consume the hooks they need.

## Structure

```typescript
// App.tsx
<LocalizationProvider dateAdapter={AdapterDateFns}>
  <ThemeProvider theme={theme}>
    <IntlProvider locale={i18nEN.locale} messages={i18nEN.messages}>
      <SnackbarProvider maxSnack={3}
        action={(key) => <Button onClick={() => closeSnackbar(key)}>Dismiss</Button>}>
        <DialogProvider>
          <BreadcrumbProvider>
            <Outlet /> {/* Routes render here */}
          </BreadcrumbProvider>
        </DialogProvider>
      </SnackbarProvider>
    </IntlProvider>
  </ThemeProvider>
</LocalizationProvider>
```

Provider responsibilities:
- `LocalizationProvider` - MUI date picker locale (date-fns)
- `ThemeProvider` - Custom MUI theme
- `IntlProvider` - react-intl translations
- `SnackbarProvider` - notistack toast notifications
- `DialogProvider` - 4 dialog types (filter, range, confirm, page)
- `BreadcrumbProvider` - Navigation history and breadcrumbs

## Examples

### ActionGroupTestReact
`App.tsx` nests 6 providers. SnackbarProvider includes a custom Dismiss button action. DialogProvider wraps 4 dialog types exposed via hooks. BreadcrumbProvider is innermost so it can access all other providers. Layout includes sidebar Navigator (permanent on desktop, temporary on mobile), Header with back button and breadcrumbs, and Copyright footer.

## Trade-offs

- **Pros**: Clean separation of concerns; each provider is independently testable; pages consume only needed hooks; standard React pattern
- **Cons**: Deep nesting can be hard to read; provider order matters; adding new providers requires modifying App.tsx; potential re-render cascades
- **When to use**: Standard pattern for JUDO React applications needing theming, i18n, notifications, and dialog support

## Related Patterns

- [promise-based-dialog-system](promise-based-dialog-system.md)
- [breadcrumb-navigation-context](breadcrumb-navigation-context.md)
- [complete-frontend-replacement](complete-frontend-replacement.md)

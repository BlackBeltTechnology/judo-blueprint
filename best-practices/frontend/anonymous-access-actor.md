---
id: "anonymous-access-actor"
title: "Anonymous Access Public-Facing Actor"
domain: "frontend"
category: "navigation"
score: 32.3
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
---
## Description

A JUDO multi-actor application where one actor allows anonymous (unauthenticated) access for public-facing functionality. The actor's `hasActorMenuAccess()` function unconditionally returns `true`, bypassing the OAuth authentication check that other actors require. This pattern is used for citizen portals, public submission forms, or any user-facing interface where login is optional. The anonymous actor typically has a minimal page set compared to authenticated actors.

## Structure

```dart
// Authenticated actor (Munkatars, Admin)
Future<bool> hasActorMenuAccess() async {
  var principal = await _actorRepository.getPrincipal();
  return principal.email.isNotEmpty;
}

// Anonymous actor (E-Ugyfel Alkalmazas)
Future<bool> hasActorMenuAccess() async {
  return true;  // Always allow access
}
```

The anonymous actor:
- Has no AuthGuard on routes (or AuthGuard is bypassed)
- Typically has fewer pages (3-5 vs 40-75 for authenticated actors)
- May have no navigation drawer items (simplified UI)
- Shares the same backend model/services as authenticated actors
- Can optionally support login for personalized features

## Examples

### kozut-eugyfel-client
E-Ugyfel Alkalmazas (E-Customer Application) actor allows anonymous access for citizens to submit and view road infrastructure reports. Only 3 pages (dashboard, table, view) vs 75 pages for Munkatars and 40 for Admin. The `hasActorMenuAccess()` always returns `true`. Munkatars and Admin actors require OAuth with principal email validation.

### kozut-eugyfel-model-test
ESM model defines the EugyfelAlkalmazas actor with minimal page set (dashboard, bejelentes table/view) and anonymous access configuration. The model-level actor definition drives the generation of simplified authentication logic in the companion Flutter client.

## Trade-offs

- **Pros**: Public-facing functionality without login barrier; shares backend with authenticated actors; simple implementation
- **Cons**: Limited functionality for anonymous users; security considerations for public endpoints; no personalization without auth
- **When to use**: Government citizen portals, public submission forms, or any scenario where some users should access the application without authentication

## Related Patterns

- [dual-actor-frontend-architecture](dual-actor-frontend-architecture.md)

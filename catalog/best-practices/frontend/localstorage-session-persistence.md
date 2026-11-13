---
id: localstorage-session-persistence
title: LocalStorage-Based Session Persistence
description: "Use `localStorage` to persist session state (user identity, current context, in-progress data) instead of OAuth/OIDC tokens or server-side sessions."
aliases: []
keywords: [localStorage, session persistence, anonymous user, kiosk, reset, client-side state]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: state
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [session-storage-table-state, email-code-guest-authentication, dialog-based-navigation, error-code-mapping-pattern]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Applications where a full sign-in is overkill (public games, event kiosks, demos) still need to remember who the visitor is and what they were doing. This practice keeps that context in the browser's `localStorage` and treats a stored identifier as the "session".

## Practice

### Platform base

- The generated frontend authenticates through the identity provider; an unauthenticated user is redirected to sign in, unless guest access is enabled and a guest page component is registered ([guest page](../../agent-docs/frontend/extension-points.md)).
- Table state (sort, filter, page size) is already persisted by the generated tables in `sessionStorage` under keys built from the table `uniqueId` ([table state persistence](../../agent-docs/frontend/extension-points.md)). Do not duplicate that.
- Access control is enforced by the backend, never by the frontend. A client-side flag only hides UI ([navigation and access hooks](../../agent-docs/frontend/hooks/navigation-and-access.md)).
- An actor marked anonymous has no principal, so what it may reach comes only from the model's access rules ([authentication guide](../../agent-docs/backend/authentication-guide.md)).

### Practice notes: a stored identifier as the session

This is practice, not a platform mechanism, and it provides no real authentication.

- Read the identity and current context from `localStorage` on start (state initialised from the stored values) and write them back in an effect when they change.
- Treat "has a stored user id" as signed in. A "Reset" action clears the storage and reloads the page.
- Use an app-specific key prefix and store ids or small JSON values only, never secrets.
- Everything the visitor may do must still be allowed by the backend for the anonymous actor; the stored id is a lookup key, not a credential.

```typescript
// Example code
const [userId, setUserId] = useState(localStorage.getItem('app-user-id'));
const [group, setGroup] = useState(JSON.parse(localStorage.getItem('app-group-id') || 'null'));

useEffect(() => {
  if (userId) localStorage.setItem('app-user-id', userId);
}, [userId]);

const handleReset = () => {
  localStorage.clear();
  window.location.reload();
};

const isAuthenticated = typeof userId === 'string';
```

## Rationale

No login screen, state survives page refreshes, and one device can serve several participants through reset. The cost is that anyone with access to the browser, or who can set the key, acts as that user. There is no server-side session check and no cross-device session.

## Example

A game frontend stores several keys (user e-mail, display name id, access code, active group as JSON, round id, round duration, prompt list and answer list as JSON). Signed in means the user id is a string; a Reset button in the bottom navigation clears everything. The code-based sign-in itself is in [[email-code-guest-authentication]].

## When to avoid

- Data or operations need real identity: use the identity provider and a principal-bound actor.
- The state must follow the user across devices.
- Table or grid state only: the generated `sessionStorage` persistence already covers it ([[session-storage-table-state]]).

## Related

- [[session-storage-table-state]] — the platform's own browser-storage persistence for tables
- [[email-code-guest-authentication]] — the code-based registration this session pattern pairs with
- [[dialog-based-navigation]] — navigation in the same participant frontend
- [[error-code-mapping-pattern]] — error handling in the same frontend

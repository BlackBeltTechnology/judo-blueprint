---
id: "derived-state-from-history"
title: "Derived State from History Trail"
domain: "model"
category: "entity"
score: 16.2
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - judo-demo-miniworkflow
alternatives:
  - enum-state-machine
---
## Description

Instead of storing the current lifecycle state directly on an entity, the state is derived from the most recent entry in a composed history collection. Each state transition creates a new immutable history entry, and the current state is computed via `self.historyEntries!head(h | h.eventTime DESC).toState`. This eliminates state synchronization issues and provides a complete audit trail as a side effect of state management.

## Structure

- Parent entity has no stored state attribute
- Parent has a composed collection of history entries (`0..*`)
- Each history entry records: `fromState` (optional, null for initial), `toState` (required), `eventTime` (timestamp), `user` (who performed it), `message` (optional)
- Derived attribute on parent: `currentState = self.historyEntries!head(h | h.eventTime DESC).toState`
- Workflow operations create new history entries rather than modifying a state field
- History entries are immutable (no CRUD)
- The `!head()` function with DESC ordering always returns the latest entry

## Examples

### judo-demo-miniworkflow
`Document.currentState` is derived: `self.documentHistoryEntries!head(h | h.eventTime DESC).toState`. Each of the 4 workflow operations (`requestReview`, `accept`, `reject`, `close`) creates a `DocumentHistoryEntry` with `fromState = this.currentState`, `toState = DocumentState#TARGET`, `eventTime = Timestamp!now()`, and `user = currentUser`. The `createDocument` factory sets the initial state to `IN_PROGRESS` by creating the first history entry. No stored state field exists on `Document`.

## Trade-offs

- Pros: No state synchronization bugs, built-in audit trail, single source of truth, every transition is automatically recorded
- Cons: Deriving state from collection requires sorting (potential performance cost), more complex than a simple stored attribute, history collection grows over time
- Prefer when: Complete audit trail of state transitions is a requirement, or when state synchronization between stored state and audit history has been a source of bugs
- Prefer [enum-state-machine](enum-state-machine.md) when: Audit trail is not needed, or performance of state reads is critical

## Related Patterns

- [enum-state-machine](enum-state-machine.md) (alternative: stored state with simpler reads)
- [audit-event-entity](audit-event-entity.md) (the history entry is an audit event)
- [composition-ownership](composition-ownership.md) (history entries are composed within the parent)
- [collection-lower-bound-zero](collection-lower-bound-zero.md) (history collection starts empty)

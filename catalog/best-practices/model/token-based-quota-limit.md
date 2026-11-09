---
id: "token-based-quota-limit"
title: "Token-Based Quota Limit Pattern"
domain: "model"
category: "entity"
score: 61.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - park-here
---
## Description

User entities define per-type numeric quota attributes (e.g., `maxNormalReservation`, `maxGuestReservation`) that limit how many active instances of a specific type a user can create. Enforcement is handled in custom operation implementations by counting active instances and comparing against the quota. Quotas are configurable per user by administrators, with sensible defaults.

## Structure

- User entity has integer attributes for each quota type, with default values
- Each quota corresponds to a category enum member (e.g., ReservationType.NORMAL -> maxNormalReservation)
- Operations check: `activeCount = user.collection!filter(status == ACTIVE and type == TYPE)!count()`
- If `activeCount >= user.maxQuota`, throw a typed error (e.g., `TOO_MANY_RESERVATION`)
- Quotas are set per user by administrators, allowing individual override
- Default values provide reasonable starting limits (e.g., 5 normal, 5 guest, 2 long-term)

## Examples

### ParkHere
User entity has 3 configurable quota attributes: `maxNormalReservation` (Integer, default: 5), `maxGuestReservation` (Integer, default: 5), `maxLongReservation` (Integer, default: 2). Each maps to a ReservationType enum member. Operations validate: count active reservations of matching type, compare against user's quota, throw `BusinessError(TOO_MANY_RESERVATION)` if exceeded. Admins can increase limits per user. Quick reservations (QUICK type) are time-limited rather than count-limited.

## Trade-offs

- Pros: Per-user configurable limits, simple enforcement logic, easy to extend with new quota types
- Cons: Quota check in operations rather than model-level validation, must remember to check in every creation path
- Prefer when: Domain requires limiting how many active instances of categorized types a user can own

## Related Patterns

- [category-enum-pattern](category-enum-pattern.md) (quota types correspond to category enum members)
- [error-code-enum-pattern](error-code-enum-pattern.md) (quota exceeded reported via error code)
- [default-value-patterns](default-value-patterns.md) (quota defaults)
- [multi-role-single-entity](multi-role-single-entity.md) (quotas stored on the same user entity as role flags)

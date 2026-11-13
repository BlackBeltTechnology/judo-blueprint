---
id: duplicate-detection-normalization
title: Duplicate Detection via Name Normalization and Similarity
description: Store a normalized copy of a name next to the display name, flag all non-archived entities that share it, and use a similarity score when checking names against an external source.
aliases: [duplicate flag, normalized name, company name matching, fuzzy name match]
keywords: [duplicate, normalization, normalizedName, similarity, Jaro-Winkler, isDuplicateName, flag, archived, DAO filter, updateAll]
tags: ["domain:backend", "layer:backend", "project:judo-partner", "status:single-project"]
category: operation
status: single-project
projects: [judo-partner]
evidence: ["judo-partner:unrecorded"]
alternatives: []
related: [soft-delete-archive-pattern, dao-fluent-query-filter, mask-field-projection]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Users type the same company or person in slightly different ways: with or without a legal form, punctuation, upper or lower case. An exact match on the display name misses these. Keep a normalized form of the name in its own attribute, find duplicates by equality on that attribute, and keep a boolean flag on each duplicate so lists and screens can show it.

## Practice

### Normalize in application code, store the result

The normalization function is plain application code (strip legal-form suffixes, punctuation, case). The platform provides no normalization or similarity function. Store the result in a `normalizedName` attribute written whenever the name changes. A stored attribute has a generated typed filter, so the lookup needs no custom query.

### Find duplicates with the typed filters

Query the DAO with `filterByNormalizedName(StringFilter.equalTo(...))` and `filterByIsArchived(BooleanFilter.isFalse())`, with a mask limited to the fields used. Typed filters chain with AND. For a boolean use `isTrue()` / `isFalse()`, not `equalTo` (see [SDK Query Filters Reference](../../agent-docs/backend/data-access-guide.md#sdk-query-filters-reference) and [Combining Multiple Filters](../../agent-docs/backend/data-access-guide.md#combining-multiple-filters)). Optional alternatives are `StringFilter.ilike` for case-insensitive comparison or a JQL `filterBy(String)` for OR conditions. A JQL filter cannot navigate relations.

### Set the flag for the whole group

After a create, update, import or archive, load the group and set `isDuplicateName` to `group.size() > 1` on every member. Update each member through the DAO with a mask for the flag only. Do not call the recalculation from the interceptor that reacts to the same update unless the flag change is skipped when unchanged, or the update triggers itself again (see [[dirty-check-before-update]]).

Recalculate for the old normalized name as well when a name changes, otherwise the former group keeps a stale flag.

### Where to hook in

Interceptors fire only for built-in operations (create, update, delete and so on). Custom operations, such as an import or validation operation, must call the recalculation themselves (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). A `postCall` hook on update is the usual place for edits made through the generated screens, and its exceptions roll back the update.

### Report duplicates, do not forbid them blindly

A duplicate is a hint, not an error. Surface the flag in the transfer object. If a hard stop is needed, raise a `ValidationException` with a `ValidationResult` code and location rather than an `IllegalStateException`, which the client receives as a generic 500 (see [Platform Exceptions](../../agent-docs/backend/error-handling-guide.md#platform-exceptions)).

### Similarity against an external source

For checking a name against an outside register, compute a similarity score (Jaro-Winkler with a chosen threshold, 0.8 in one application) in application code and use it as a warning. Tune the threshold on real data, because false positives and negatives are both likely.

## Rationale

- Equality on a stored normalized value is one query, cheaper than comparing every pair of names.
- The flag turns an expensive check into a column that lists can filter and show.
- Limit: normalization rules are domain-specific (here legal forms of one country), and the group recalculation grows with the number of duplicates.

## Example

A utility normalizes a company name by removing legal-form suffixes and punctuation and upper-casing it. A service queries all non-archived records with the same normalized name, sets the duplicate flag on each, and updates them in one batch. It runs after create, validate and delete operations and in the record update interceptor. A separate function compares the name with an external register using Jaro-Winkler and a 0.8 threshold.

## When to avoid

- Names are already unique by an identifier such as a tax number: use a uniqueness check on that.
- The data set is small and a reviewer can scan it: a plain list is enough.
- Fuzzy matching is the core need: use database-level trigram or phonetic matching, which this pattern does not provide.

## Related

- [[soft-delete-archive-pattern]] — archived entities are excluded from the duplicate group
- [[dao-fluent-query-filter]] — typed DAO filters used to find the group
- [[mask-field-projection]] — limiting the loaded fields
- [[dirty-check-before-update]] — avoiding needless flag writes

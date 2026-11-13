---
id: feed-targeting-strategy
title: Pluggable Feed Targeting Strategy Pattern
description: "A strategy interface, registered as OSGi components, that decides which tenants or users see a piece of feed content."
aliases: [feed targeting, audience strategy]
keywords: [pluggable, feed, targeting, strategy, osgi, dao]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: service
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/feed/AllActiveOrganizationsTargetingStrategy.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/feed/RequestTargetingStrategy.java"]
alternatives: [service-delegation-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Content in a feed must reach different audiences depending on its type: Notice goes to every active account, a Request only to accounts with matching capabilities. A strategy interface keeps the targeting rules out of the feed service, so a new content type adds a strategy and does not change the feed logic.

## Practice

### Strategy interface with OSGi implementations

This is a convention built on platform mechanisms: OSGi components with `@Reference` injection and generated DAOs with the fluent query builder (see [data access guide](../../agent-docs/backend/data-access-guide.md) and [patterns and best practices](../../agent-docs/backend/patterns-and-best-practices.md)). The platform has no feed or strategy concept.

- The interface offers a target-determination method and a target-filtering method.
- Each implementation is an OSGi component injecting the DAOs it needs and building its candidate list with the generated query API (`filterBy...` with filter classes such as `EnumerationFilter`, ended by `selectList()`).
- The feed service (an example service) picks the strategy by content type and calls it.

```java
// Example code: FeedTargetingStrategy, Account, Post, Request are types
public interface FeedTargetingStrategy {
    List<Account> determineTargets(Post post);
    List<Account> filterTargets(FeedEntry entry, List<Account> candidates);
}

@Component(immediate = true, service = FeedTargetingStrategy.class)
public class AllActiveAccountsTargetingStrategy implements FeedTargetingStrategy {
    @Reference AccountDao accountDao;

    public List<Account> determineTargets(Post post) {
        return accountDao.query()
            .filterByStatus(EnumerationFilter.equalTo(AccountStatus.ACTIVE))
            .selectList();
    }
}

// the feed service selects by content type
FeedTargetingStrategy strategy = post instanceof Request
    ? requestTargetingStrategy : allActiveAccountsTargetingStrategy;
List<Account> targets = strategy.determineTargets(post);
```

### Select the strategy explicitly

Because several components provide the same service interface, inject each concrete strategy by its own type or collect them and choose by content type. The selection logic is the one place to change when a content type is added.

## Rationale

- Targeting rules are isolated and testable, and the feed service stays closed for modification.
- Broadcast and targeted distribution use the same call.
- Cost: the selection logic must be maintained per content type, and a capability-matching strategy that loads all active accounts and filters in memory does not scale; push such filters into the query where the model allows it.

## Example

One application has two strategies. One broadcasts to all active accounts (Notice, Promotion, Announcement), the other targets only accounts with matching capabilities (Request). The feed service can also re-run the strategy to add newly created accounts to existing feed entries.

## When to avoid

- One content type with one fixed audience: a plain service method is enough.
- Targeting that the database can express as a single filter: use a query filter ([[dao-fluent-query-filter]]).

## Related

- [[service-delegation-pattern]] — operations delegate to the feed service
- [[dao-fluent-query-filter]] — the query API the strategies use
- [[state-lifecycle-operation]] — publishing that triggers targeting

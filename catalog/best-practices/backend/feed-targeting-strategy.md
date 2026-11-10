---
id: feed-targeting-strategy
title: Pluggable Feed Targeting Strategy Pattern
description: "A project-level strategy interface, registered as OSGi components, that decides which organizations or users see a piece of feed content."
aliases: [feed targeting, audience strategy]
keywords: [pluggable, feed, targeting, strategy, osgi, dao]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: service
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: [service-delegation-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Content in a feed must reach different audiences depending on its type: News goes to every active organization, a Request only to organizations with matching capabilities. A strategy interface keeps the targeting rules out of the feed service, so a new content type adds a strategy and does not change the feed logic.

## Practice

### Strategy interface with OSGi implementations

This is project practice built on platform mechanisms: OSGi components with `@Reference` injection and generated DAOs with the fluent query builder (see [data access guide](../../agent-docs/backend/data-access-guide.md) and [patterns and best practices](../../agent-docs/backend/patterns-and-best-practices.md)). The platform has no feed or strategy concept.

- The interface offers a target-determination method and a target-filtering method.
- Each implementation is an OSGi component injecting the DAOs it needs and building its candidate list with the generated query API (`filterBy...` with filter classes such as `EnumerationFilter`, ended by `selectList()`).
- The feed service (an example project service) picks the strategy by content type and calls it.

```java
// Example project code: FeedTargetingStrategy, Organization, Post, Request are project types
public interface FeedTargetingStrategy {
    List<Organization> determineTargets(Post post);
    List<Organization> filterTargets(FeedEntry entry, List<Organization> candidates);
}

@Component(immediate = true, service = FeedTargetingStrategy.class)
public class AllActiveOrganizationsTargetingStrategy implements FeedTargetingStrategy {
    @Reference OrganizationDao organizationDao;

    public List<Organization> determineTargets(Post post) {
        return organizationDao.query()
            .filterByStatus(EnumerationFilter.equalTo(OrganizationStatus.ACTIVE))
            .selectList();
    }
}

// the feed service selects by content type
FeedTargetingStrategy strategy = post instanceof Request
    ? requestTargetingStrategy : allActiveOrganizationsTargetingStrategy;
List<Organization> targets = strategy.determineTargets(post);
```

### Select the strategy explicitly

Because several components provide the same service interface, inject each concrete strategy by its own type or collect them and choose by content type. The selection logic is the one place to change when a content type is added.

## Rationale

- Targeting rules are isolated and testable, and the feed service stays closed for modification.
- Broadcast and targeted distribution use the same call.
- Cost: the selection logic must be maintained per content type, and a capability-matching strategy that loads all active organizations and filters in memory does not scale; push such filters into the query where the model allows it.

## Example

mlszksz-platform has two strategies. One broadcasts to all active organizations (News, Offer, Announcement), the other targets only organizations with matching capabilities (Request). The feed service can also re-run the strategy to add newly created organizations to existing feed entries.

## When to avoid

- One content type with one fixed audience: a plain service method is enough.
- Targeting that the database can express as a single filter: use a query filter ([[dao-fluent-query-filter]]).

## Related

- [[service-delegation-pattern]] — operations delegate to the feed service
- [[dao-fluent-query-filter]] — the query API the strategies use
- [[state-lifecycle-operation]] — publishing that triggers targeting

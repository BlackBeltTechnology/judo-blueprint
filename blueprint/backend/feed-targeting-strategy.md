---
id: "feed-targeting-strategy"
title: "Pluggable Feed Targeting Strategy Pattern"
domain: "backend"
category: "service"
score: 13.1
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - mlszksz-platform
---
## Description

A Strategy pattern for determining which organizations or users should see a piece of content in a feed system. The `FeedTargetingStrategy` interface defines `determineTargets()` and `filterTargets()` methods, with pluggable implementations registered as OSGi components. The `FeedService` selects the appropriate strategy based on content type, enabling different targeting rules without modifying core feed logic.

## Structure

```java
// Strategy interface
public interface FeedTargetingStrategy {
    List<Organization> determineTargets(Post post);
    List<Organization> filterTargets(FeedEntry entry, List<Organization> candidates);
}

// Broadcast strategy (all active orgs)
@Component(immediate = true, service = FeedTargetingStrategy.class)
public class AllActiveOrganizationsTargetingStrategy implements FeedTargetingStrategy {
    @Reference OrganizationDao organizationDao;

    @Override
    public List<Organization> determineTargets(Post post) {
        return organizationDao.query()
            .filterByStatus(EnumerationFilter.equalTo(OrganizationStatus.ACTIVE))
            .selectList();
    }
}

// Capability-matching strategy
@Component(immediate = true, service = FeedTargetingStrategy.class)
public class RequestTargetingStrategy implements FeedTargetingStrategy {
    @Override
    public List<Organization> determineTargets(Request request) {
        List<Capability> required = requestDao.queryCapabilities(request).selectList();
        return organizationDao.query()
            .filterByStatus(EnumerationFilter.equalTo(OrganizationStatus.ACTIVE))
            .selectList().stream()
            .filter(org -> hasMatchingCapabilities(org, required))
            .collect(Collectors.toList());
    }
}

// FeedService selects strategy by content type
FeedTargetingStrategy strategy = post instanceof Request
    ? requestTargetingStrategy : allActiveOrganizationsTargetingStrategy;
List<Organization> targets = strategy.determineTargets(post);
```

## Examples

### mlszksz-platform
Two strategies: `AllActiveOrganizationsTargetingStrategy` (broadcasts to all active orgs, used for News/Offer/Announcement) and `RequestTargetingStrategy` (targets only orgs with matching capabilities, used for Request posts). FeedService also supports `syncAllFeed()` which retroactively adds new organizations to existing feed entries using the appropriate strategy.

## Trade-offs

- Pros: Open for extension (new strategies without modifying FeedService), clean separation of targeting logic, supports both broadcast and targeted distribution
- Cons: Strategy selection logic must be maintained when new content types are added, capability matching loads all orgs then filters in memory
- Alternative: Database-level targeting via SQL views, event-driven pub/sub, or model-level filter expressions

## Related Patterns

- service-delegation-pattern
- dao-fluent-query-filter
- state-lifecycle-operation

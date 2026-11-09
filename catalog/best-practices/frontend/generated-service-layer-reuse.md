---
id: "generated-service-layer-reuse"
title: "Reusing Generated TypeScript Service Layer in Custom UI"
domain: "frontend"
category: "mapping"
score: 38.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - actiongroup-test-react
---
## Description

When replacing the generated JUDO UI with a custom frontend, continue to import and use the generated TypeScript service implementations (Axios-based REST clients) and transfer object type definitions. This gives custom UIs type-safe API access, consistent error handling, and query customizer support without reimplementing the API layer.

## Structure

```typescript
// Instantiate generated service in custom component
const playerServiceForContestsImpl = useMemo(
  () => new PlayerServiceForContestsImpl(judoAxiosProvider), []
);

// Use generated transfer object types
const [contests, setContests] = useState<ActorsplayerContestStored[]>([]);

// Call service methods with type-safe parameters
const data = await playerServiceForContestsImpl.list(
  undefined,
  { _mask: '{title,description}' } as QueryCustomizer<ActorsplayerContest>
);
```

Services are generated under `src/services/` and remain in the generator's scope (not ignored).

## Examples

### Trivia
Player frontend instantiates 4 generated services via `useMemo`: `ActorsplayerContestServiceImpl` (contest entry), `PlayerServiceForContestsImpl` (listing, scoreboard), `PlayerServiceForTestsImpl` (quiz flow), and `PlayerServiceForApplicationImpl` (registration/activation). All use `judoAxiosProvider` for HTTP transport.

### ActionGroupTestReact
Imports generated Axios services directly: `godServiceForGalaxiesImpl` (root CRUD), `viewGalaxyServiceImpl` (entity view), `viewGalaxyServiceForStarsImpl` (nested entity), `viewGalaxyServiceForMatterImpl` (many-aggregation). Also uses generated types (`ViewGalaxyStored`, `ViewGalaxyQueryCustomizer`) and mask builders (`ViewGalaxyMaskBuilder`).

## Trade-offs

- **Pros**: Type-safe API calls; no manual REST client code; consistent with backend API changes; query customizer support for filtering/sorting
- **Cons**: Couples custom UI to generated service interfaces; service API changes require regeneration
- **When to use**: Always, when building custom UI within a JUDO project -- there is no reason to bypass the generated service layer

## Related Patterns

- [complete-frontend-replacement](complete-frontend-replacement.md)
- [error-code-mapping-pattern](error-code-mapping-pattern.md)

---
id: "custom-jaxrs-sse-endpoint"
title: "Custom JAX-RS Endpoint with Server-Sent Events on JUDO-Karaf"
domain: "backend"
category: "integration"
score: 0
usage_count: 1
alternative_count: 0
first_seen: "2026-05-12"
last_updated: "2026-05-12"
projects:
  - compsych-letter-demo
alternatives: []
---

## Description

Add a hand-written JAX-RS REST resource **alongside** the JUDO-generated
REST stack, with support for streaming responses via Server-Sent Events
(`text/event-stream`). The use case in `compsych-letter-demo` is the
AI agent console endpoint (`/api/agent/chat/*`): JUDO's generated REST
emits unary request/response operations only, but the agent UI needs an
SSE stream of `token`/`tool_call`/`tool_result`/`message_end`/`error`
envelopes.

This pattern uses three coordinated pieces on top of the platform's
`hu.blackbelt.cxf:cxf-jaxrs-application-manager` + CXF 3.5.6 stack:

1. A `javax.ws.rs.core.Application` `@Component` declaring the mount
   path via `applicationPath` service property + `@ApplicationPath`
   annotation.
2. A `@Path`-annotated `@Component` resource class wired into the
   application's `getSingletons()` via `@Reference`.
3. The optional `cxf-rt-rs-sse` bundle added to the feature, since the
   platform's `judo-platform-cxf-jaxrs` ships `cxf-rt-frontend-jaxrs`
   only.

## Anti-Patterns (don't do these)

- **`hu.blackbelt.cxf:cxf-jaxrs-application-manager` `BasicApplication`
  via `.cfg` file in `application/karaf-features/etc/`.** Documented in
  the upstream `cxf-jaxrs-application-manager` README, but this
  project's `karaf-offline` assembly does NOT package
  `karaf-features/etc/*.cfg` into the runtime Karaf `etc/`. The
  `BasicApplication` config has `configurationPolicy=REQUIRE`, so
  without the cfg actually deployed the application silently never
  activates. Existing LLM/converter `.cfg` files in the same project
  only "work" because their consuming components use
  `configurationPolicy=OPTIONAL` and start with their
  `@Component property` defaults; `BasicApplication` has no such
  fallback.
- **Register only the resource class, expect platform tracker to pick
  up the path.** The JUDO platform's
  `hu.blackbelt.judo.services.cxf.osgi.CxfActivator` (and the
  underlying CXF bus) tracks `@Path`-annotated OSGi `@Component`
  services and mounts them at the CXF servlet root (`/api`). Without a
  matching `Application` service property `applicationPath=/something`,
  the publish address defaults to `/` and the endpoint ends up at
  `/api/<class-level-@Path>` instead of `/api/<intended-prefix>/<...>`.
  You see `No @ApplicationPath found on component, service.id = N`
  warnings in `console.out`.
- **Karaf `<feature>cxf-rt-rs-sse</feature>` reference.** No such
  feature exists in `judo-platform-karaf-features` of any vintage. SSE
  ships as a CXF bundle (`org.apache.cxf:cxf-rt-rs-sse:<cxf-version>`),
  not as a Karaf feature.
- **Direct edit of `application/karaf-features/src/main/feature/feature.xml`.**
  Overwritten on every `./judo.sh build` / `judo.sh generate`. Use the
  fragment-override hook (see `karaf-customization-via-fragments`).
- **Class-level `@Path` that duplicates the applicationPath segment.**
  If `Application` mounts at `/agent` and the resource carries
  `@Path("/agent/chat")`, the actual URL becomes `/api/agent/agent/chat`
  (CXF servlet context + applicationPath + class-level `@Path`). Keep
  the class `@Path` short and segment-only (`@Path("/chat")` in this
  example).

## Structure

### 1. JAX-RS Application `@Component`

`application/internal/src/main/java/.../integrations/agent/AgentRestApplication.java`:

```java
package hu.blackbelt.compsych.letter.integrations.agent;

import java.util.Set;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;

import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;

@Component(
        service = Application.class,
        immediate = true,
        property = {
                "applicationPath=/agent",
                "jaxrs.application.name=agent"
        })
@ApplicationPath("/agent")
public class AgentRestApplication extends Application {

    @Reference
    private AgentRestResource resource;

    @Override
    public Set<Object> getSingletons() {
        return Set.of(resource);
    }
}
```

Key points:

- `service = Application.class` — the platform's CXF
  `ApplicationStore.ApplicationTracker` only sees services registered
  under `javax.ws.rs.core.Application`. Without this, the component is
  invisible to the tracker.
- **Both** the `property = {"applicationPath=/agent", ...}` OSGi
  service property AND the `@ApplicationPath("/agent")` JAX-RS
  annotation should be set. The platform reads the OSGi property
  first; CXF and downstream tooling (WADL, service list) read the
  annotation. Keeping them consistent avoids the `No @ApplicationPath
  found on component` warning and ensures the path appears in the
  service list at `http://localhost:8181/api/services`.
- `getSingletons()` returns the resource instance injected via
  `@Reference`, so DS-managed `@Reference`s inside the resource are
  resolved before it joins the JAX-RS runtime.

### 2. JAX-RS Resource `@Component`

Same package, `AgentRestResource.java`:

```java
@Component(service = AgentRestResource.class, immediate = true)
@Path("/chat")
public class AgentRestResource {

    @Reference
    private ChatSessionStore sessionStore;

    @Reference
    private AgentTools agentTools;

    @Reference(target = "(profile=stub)")
    private LlmProvider llmProvider;

    @POST
    @Path("")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response start(...) { ... }

    @POST
    @Path("/{sessionId}/messages")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.SERVER_SENT_EVENTS)
    public void messages(
            @PathParam("sessionId") final String sessionId,
            @HeaderParam(HttpHeaders.AUTHORIZATION) final String authorization,
            @Context final SseEventSink sink,
            @Context final Sse sse,
            final InputStream body) { ... }

    @DELETE
    @Path("/{sessionId}")
    public Response close(@PathParam("sessionId") final String sessionId) { ... }
}
```

Key points:

- `service = AgentRestResource.class` exposes the resource as an OSGi
  service so the application can `@Reference` it. It also makes the
  resource visible to the platform's `@Path` tracker; this is harmless
  because the application path takes precedence at the servlet level.
- Class-level `@Path("/chat")` is the resource sub-path under the
  application's mount. URL math:
  `(CXF servlet context: /api) + (applicationPath: /agent) + (class @Path: /chat)`
  → `/api/agent/chat`.
- The SSE method takes `@Context SseEventSink sink, @Context Sse sse`
  arguments and returns `void`; CXF flushes events as they're sent.
  The method MUST be annotated `@Produces(MediaType.SERVER_SENT_EVENTS)`.

### 3. Maven dependency (compile-time)

`application/internal/pom.xml` needs the JAX-RS API including
`javax.ws.rs.sse.*`. Since the upstream `internal/pom.xml.hbs`
template does NOT expose an `extra-dependencies.fragment.hbs` slot,
add `internal/pom.xml` to `application/.generator-ignore` (see
`generator-ignore-config-protection`) and add the dependency directly:

```xml
<dependency>
    <groupId>jakarta.ws.rs</groupId>
    <artifactId>jakarta.ws.rs-api</artifactId>
    <version>2.1.6</version>
    <scope>provided</scope>
</dependency>
```

`provided` is correct — the platform ships `jakarta.ws.rs-api/2.1.6`
via the `judo-platform-cxf-jaxrs` feature at runtime, so the bundle
manifest's `Import-Package` entry `javax.ws.rs;version="[2.1,3)"` (and
`javax.ws.rs.sse`) wires through.

### 4. Karaf feature — SSE runtime bundle

`cxf-rt-frontend-jaxrs` is in the platform feature, but `cxf-rt-rs-sse`
is NOT. Add it via the fragment-override hook (use the centralized
layout per `karaf-customization-via-fragments`):

`application/generator-overrides/karaf-features/src/main/feature/feature.xml.extra-bundles.fragment.hbs`:

```xml
        <!--
            Server-Sent Events provider for the AI agent REST endpoint.
            cxf-jaxrs (3.5.6) ships transitively via the platform feature
            judo-platform-cxf-jaxrs but cxf-rt-rs-sse is a separate Apache
            CXF bundle that is NOT included in the JUDO karaf-features
            distribution.
        -->
        <bundle>mvn:org.apache.cxf/cxf-rt-rs-sse/3.5.6</bundle>
```

Pin the CXF version to whatever `cxf-rt-frontend-jaxrs` ships at — for
the 2026.03 platform that is 3.5.6. After `./judo.sh generate` the
regenerated `application/karaf-features/src/main/feature/feature.xml`
will carry the inlined `<bundle>` line; the `karaf-offline` assembly
then packages `cxf-rt-rs-sse-3.5.6.jar` into
`application/karaf-offline/target/assembly/system/org/apache/cxf/cxf-rt-rs-sse/3.5.6/`.

### 5. Smoke test recipe

Once Karaf is running and the bundle is deployed, verify the endpoint:

```bash
# Endpoint should appear in the CXF service list
curl -sS http://localhost:8181/api/services | grep agent

# Without auth → 401 from the JWT extractor (proves the endpoint is mounted)
curl -sS -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8181/api/agent/chat
# → 401

# WADL surface
curl -sS "http://localhost:8181/api/agent?_wadl"
```

For a token-driven end-to-end smoke (Keycloak password grant + start +
SSE stream + close), see the project's
`docs/judo-karaf-runtime-notes.md` or the e2e-testing skill.

## Examples

### compsych-letter-demo — AI agent console (Wave I.5)

The endpoint surface mounted at `/api/agent/chat`:

- `POST /api/agent/chat` — body `{contextRef: {kind, id, activeLang?}}`,
  returns `{sessionId}`.
- `POST /api/agent/chat/{sessionId}/messages` — body `{text}`,
  response `text/event-stream` emitting envelopes
  (`token` / `tool_call` / `tool_result` / `context_diff` /
  `message_end` / `error`).
- `DELETE /api/agent/chat/{sessionId}` — close session.

Surrounding pieces: an in-memory `ChatSessionStore` with 20-minute
idle TTL sweeper, a stub `AgentTools` registry exposing six
`ToolDescriptor`s with no-op executors (real wiring deferred to
Wave-3 follow-up), a `JwtClaims` helper that decodes
`preferred_username` from the bearer header. See openspec change
`wire-agent-rest-endpoint` for the full design + verification record.

Observed quirks during apply-time verification:

- `applicationPath=/agent` OSGi property alone produced
  `No @ApplicationPath found on component, service.id = N` warnings in
  `console.out`; adding the `@ApplicationPath("/agent")` JAX-RS
  annotation in addition silenced the warning AND made the mount path
  appear correctly in the CXF service list.
- The first attempted class-level `@Path("/agent/chat")` (without
  realising the applicationPath would also contribute `/agent`)
  produced `http://localhost:8181/api/agent/agent/chat` — fixed by
  changing the class `@Path` to `/chat`.
- `bundle:watch` reload of the `internal` bundle broke ALL components
  in the bundle with a `BusinessErrorException` `ClassNotFoundException`
  cascading from a split-package wiring shift. Cold restart fixes it.
  See `osgi-karaf-bundle-architecture` → "Hot-Reload Caveats" for the
  full diagnosis.

## Trade-offs

- **Pros**: full SSE / streaming surface, complete control over auth
  handling (the resource reads the bearer header directly), no
  coupling to JUDO's generated REST conventions, fits naturally
  alongside JUDO-generated REST at the same CXF servlet root.
- **Cons**: bypasses JUDO's REST API governance — no OpenAPI doc
  emission, no automatic CORS handling (relies on the platform's
  global CORS provider), no auto-wired `BusinessErrorException`
  marshalling (the resource must catch and convert to HTTP responses
  itself); split-package gotcha (see above) requires either a clean
  hand-stub design or cold-restart discipline; `bundle:watch` is
  unreliable for the resource's owning bundle.
- **Alternative**: a JUDO custom operation declared in the model.
  Use this when the surface fits the unary request/response shape and
  doesn't need streaming or per-session state. SSE / streaming is the
  only reason to step outside the generated REST stack.

## Related Patterns

- [karaf-customization-via-fragments](karaf-customization-via-fragments.md) — adds the `cxf-rt-rs-sse` bundle via the fragment override.
- [osgi-karaf-bundle-architecture](osgi-karaf-bundle-architecture.md) — hot-reload caveats that bite this pattern in particular.
- [generator-ignore-config-protection](generator-ignore-config-protection.md) — needed for the `internal/pom.xml` jakarta-ws-rs-api dependency.
- [custom-operation-osgi-component](custom-operation-osgi-component.md) — the generated-REST alternative for unary operations.

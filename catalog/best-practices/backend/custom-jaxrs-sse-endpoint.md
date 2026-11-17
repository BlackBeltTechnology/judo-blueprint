---
id: custom-jaxrs-sse-endpoint
title: Custom JAX-RS Endpoint with Server-Sent Events on JUDO-Karaf
description: "A hand-written JAX-RS resource mounted next to the generated REST stack, used when an endpoint must stream Server-Sent Events, which generated unary operations cannot do."
aliases: [SSE endpoint, streaming endpoint, custom REST resource]
keywords: [JAX-RS, SSE, text/event-stream, CXF, Application, applicationPath, cxf-rt-rs-sse, streaming, Karaf]
tags: ["domain:backend", "layer:backend", "project:compsych-letter-demo", "status:single-project"]
category: integration
status: single-project
projects: [compsych-letter-demo]
evidence: ["compsych-letter-demo:unrecorded"]
alternatives: []
first_seen: 2026-05-12
last_updated: 2026-11-10
---
## Intent

Add a hand-written JAX-RS resource alongside the generated REST stack to stream responses as Server-Sent Events (`text/event-stream`). The generated REST emits unary request/response operations only; an AI agent console needed a stream of `token`, `tool_call`, `tool_result`, `message_end` and `error` envelopes.

## Practice

### Platform base

- Generated JAX-RS services are rooted at `/api/<Model>/...` and forward to the dispatcher ([platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md#rest-wire-contract)).
- A custom endpoint is an OSGi DS component annotated `@Path`, bound into a `BasicApplication` of `cxf-jaxrs-application-manager` through a `jaxrs.resource.components` LDAP filter or a `jaxrs.resource.classes` list ([custom REST endpoints and CXF](../../agent-docs/backend/platform-behavior-reference.md#custom-rest-endpoints-and-cxf)). Custom `@Provider` classes need `X-JAXRS-Provider: true` in the bundle manifest.
- Extra Karaf bundles, extra Maven dependencies and OSGi configuration reach the generated modules through fragment overrides ([extending generated files](../../agent-docs/deployment/build-process.md#extending-generated-files-via-fragment-overrides)); see [[karaf-customization-via-fragments]].
- A custom endpoint is outside the dispatcher: no interceptor, access rule or modeled-fault mapping applies to it. The resource handles authentication and error responses itself. (Inferred from the endpoint not going through the dispatcher; *verify*.)
- The platform docs do not mention SSE, `cxf-rt-rs-sse` or the CXF version; everything below on those is observation from one application, *verify* against your platform version.

### Practice notes: Application component plus resource component

Three coordinated pieces, all application code in one example (not platform API):

1. A `javax.ws.rs.core.Application` `@Component` that declares the mount path with the `applicationPath` service property **and** the `@ApplicationPath` annotation, and returns the injected resource from `getSingletons()`.
2. A `@Path` resource `@Component` whose class-level path is only the segment below the application path.
3. The `cxf-rt-rs-sse` bundle added to the Karaf feature, because the platform CXF JAX-RS feature (CXF 3.5.6 in the observed 2026.03 platform) carries the JAX-RS frontend but not the SSE provider.

```java
// Example code
@Component(service = Application.class, immediate = true,
           property = { "applicationPath=/agent", "jaxrs.application.name=agent" })
@ApplicationPath("/agent")
public class AgentRestApplication extends Application {
    @Reference private AgentRestResource resource;
    @Override public Set<Object> getSingletons() { return Set.of(resource); }
}

@Component(service = AgentRestResource.class, immediate = true)
@Path("/chat")
public class AgentRestResource {
    @Reference private SessionStore sessionStore;

    @POST @Path("/{sessionId}/messages")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.SERVER_SENT_EVENTS)
    public void messages(@PathParam("sessionId") String sessionId,
                         @HeaderParam(HttpHeaders.AUTHORIZATION) String authorization,
                         @Context SseEventSink sink, @Context Sse sse,
                         InputStream body) { /* send events, close sink */ }
}
```

- `service = Application.class` is what makes the Application visible to the platform's application tracker (observed).
- Set both the service property and the annotation: with the property alone the example saw `No @ApplicationPath found on component` warnings, and the annotation made the path appear in the CXF service list.
- URL = CXF servlet root (`/api`) + application path (`/agent`) + class path (`/chat`) = `/api/agent/chat`. A class-level `@Path("/agent/chat")` produced `/api/agent/agent/chat`.
- The SSE method takes `SseEventSink` and `Sse` as `@Context` arguments, returns `void`, and must be `@Produces(MediaType.SERVER_SENT_EVENTS)`.
- Exposing the resource as its own OSGi service lets the Application `@Reference` it; DS resolves the resource's references before it joins the JAX-RS runtime.
- Compile dependency: the JAX-RS API (including `javax.ws.rs.sse`) as `provided`; the runtime supplies `jakarta.ws.rs-api` 2.1.6 through the platform feature. The upstream `internal` pom template had no dependency fragment slot (observed), so the application listed that pom in `.generator-ignore` ([[generator-ignore-config-protection]]).
- Runtime: a single `<bundle>mvn:org.apache.cxf/cxf-rt-rs-sse/<cxf-version>` line in the `extra-bundles` fragment, pinned to the CXF version of the platform feature. No Karaf feature named `cxf-rt-rs-sse` exists in the platform features (observed).
- Smoke test: the endpoint shows up in the CXF service list at `/api/services` and a `?_wadl` request, and an unauthenticated POST returns 401 from the JWT extractor, which proves the mount.

### Do not

- Configure `BasicApplication` through a `.cfg` file in `karaf-features/etc/`: that component requires its configuration, and the application's offline assembly did not package that directory, so the application silently never activated. (Compare the `.cfg` caveat in [[karaf-customization-via-fragments]].)
- Register only the resource class and expect a path: without an Application `applicationPath` the endpoint lands at `/api/<class @Path>`.
- Hand-edit the generated `feature.xml`: it is regenerated; use the fragment hook.

## Rationale

- Full SSE and streaming surface, direct control over bearer-header handling, no coupling to generated REST conventions, same CXF servlet root as generated REST.
- Cost: no OpenAPI document, no modeled-fault marshalling (the resource converts failures to HTTP responses itself), and relying on the platform CORS provider. Hot reload of the owning bundle broke every component in it with a `ClassNotFoundException` on the application's fault exception class (split-package wiring shift); a cold restart fixed it ([[osgi-karaf-bundle-architecture]]).
- Alternative: a custom operation declared in the model ([[custom-operation-osgi-component]]) whenever the surface fits unary request/response and needs no streaming or per-session state.

## Example

The example agent console at `/api/agent/chat`:

- `POST /api/agent/chat` takes a context reference and returns a session id.
- `POST /api/agent/chat/{sessionId}/messages` takes the text and streams `token`, `tool_call`, `tool_result`, `context_diff`, `message_end` and `error` envelopes.
- `DELETE /api/agent/chat/{sessionId}` closes the session.

Surrounding pieces: an in-memory session store with a 20-minute idle sweeper, a stub tool registry of six no-op tool descriptors, and a helper that reads `preferred_username` from the bearer token.

## When to avoid

- The surface is unary request/response: use a modeled custom operation, which keeps interceptors, access and fault mapping.
- You cannot tolerate bypassing the generated REST governance (no OpenAPI, own auth handling).

## Related

- [[karaf-customization-via-fragments]] — adds the SSE bundle through the fragment override
- [[osgi-karaf-bundle-architecture]] — hot-reload caveats that bite this pattern
- [[generator-ignore-config-protection]] — protects the hand-edited internal pom
- [[custom-operation-osgi-component]] — the generated-REST alternative for unary operations

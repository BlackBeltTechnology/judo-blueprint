---
id: structure-non-java-service-folders
title: Folders for Non-Java Services and Images Under application/
description: Practice for placing non-bundle parts of a JUDO application (a Python HTTP service, an identity-provider theme image, an externally built plugin image) as self-contained folders beside the Maven modules, built as images and wired through the docker module's compose files.
aliases: [sidecar folder, non-Java module, docker-only module, side service layout]
keywords: [sidecar, docker, compose, image, Dockerfile, python, keycloak theme, plugin, profile, skipDocker, exec-maven-plugin, structure, module]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/md-document-converter/AGENTS.md", "rackinspect:application/keycloak-theme/Dockerfile", "rackinspect:application/rackinspect-pi-analyzer-plugin/pom.xml", "rackinspect:application/docker/AGENTS.md", "rackinspect:application/generator-overrides/pom.xml.extra-profiles.fragment.hbs"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Not every part of an application is an OSGi bundle. A document converter in Python, a login theme or an AI service run as separate containers. Give each its own folder under `application/` with everything needed to build its image, and connect it to the backend only over HTTP and through the compose files, so the Karaf build never depends on another toolchain.

## Practice

### Platform base

- The generated `docker` module builds the backend image with Jib and is part of the `build-docker` profile, skipped with `-DskipDocker`; the launcher script's default build passes that flag ([Docker image build](../../agent-docs/deployment/build-process.md#docker-image-build), [build profiles](../../agent-docs/deployment/build-process.md#build-profiles)).
- The generated `keycloak-theme` module is a generation toggle that holds FreeMarker login pages ([custom Keycloak login theme](../../agent-docs/deployment/generator-plugins.md#custom-keycloak-login-theme)).
- The platform defines no sidecar services; publishing, naming and compose wiring are application practice.

### Practice notes: one folder per image, three build styles

```
application/
├── docker/                       generated module + compose-local/, compose-develop/, compose-e2e/
├── <converter>/                  not a Maven module
│   ├── Dockerfile
│   ├── AGENTS.md                 purpose, invariants, how to build and test
│   ├── app.py, <package>/, tests/, requirements*.txt
│   └── VENDOR.md, CHANGES.md     origin and local deviations of vendored code
├── <idp-theme>/                  not a Maven module
│   ├── Dockerfile                FROM the identity-provider image, COPY the theme
│   └── <theme>/login/, email/
└── <plugin>/                     Maven module, packaging pom, own profile
    ├── pom.xml                   unpack published artifact, then docker build
    └── README.md
```

| Style | When | Built by |
|---|---|---|
| Plain folder with `Dockerfile` | own source in another language, or a theme | `docker build <folder>`; compose refers to the image by a variable with a local default |
| Maven `pom` module in its own profile | an artifact published elsewhere that must become an image in the same version as the app | `maven-dependency-plugin` unpack, then `exec-maven-plugin` runs `docker build`; profile activated by `!skipDocker` and added through the root `extra-profiles` fragment |
| Generated module | the backend image | the generated `docker` module |

Rules:

- **Self-contained folder.** Source, Dockerfile, tests, dependency list and an `AGENTS.md` or README sit in the folder; nothing outside it is needed to build the image.
- **One version source.** The image tag comes from one place (a property in the module pom, or a compose variable), and scripts read it from there.
- **Keep the Karaf build free of other toolchains.** A plain build and CI without Docker or npm must still pass; image modules activate only with the Docker profile.
- **No sibling paths in Java tests.** A backend test that reads a template from the converter folder by relative path ties both folders to their current place; ship the template with the request or copy it into the test module.
- **Wire in compose, not in code.** Each compose stack in the `docker` module names the image (`${CONVERTER_IMAGE:-<app>/<converter>:local}`) and passes the URL to the backend through an environment variable; the backend reads it as OSGi configuration ([[karaf-customization-via-fragments]]).
- **Theme image versus generated theme module.** A plain image `FROM` the identity-provider base with the theme copied in is simpler than the generated Maven module when the theme is maintained by hand. Then make sure the generated theme module does not produce a second theme; *verify* its generation toggle in the generator parameters.

## Rationale

- Each image builds with its own toolchain, so a Python or Node change never touches the Maven reactor.
- Local notes (`VENDOR.md`, `CHANGES.md`) make vendored code and its deliberate deviations reviewable.
- Cost: compose files, environment variable names and image tags must be kept in sync by hand; several compose stacks multiply that.

## Example

One application has three such folders. A Python Markdown-to-DOCX-to-PDF converter folder with its own Dockerfile, tests and vendoring notes; the compose stacks refer to it through an image variable with a `:local` default, and the backend report library sends it Markdown over HTTP. A theme folder whose Dockerfile copies the login and e-mail theme onto the identity-provider base image. An AI plugin module of packaging `pom` that unpacks a zip published by another repository and builds its image; it is registered in the `extra-profiles` fragment, active only when Docker images are built, and its version property is the single source the start script reads.

## When to avoid

- The code can run inside Karaf as a bundle with acceptable dependencies: make it a module, not a service.
- A one-off script used only at development time belongs in a tools folder, not in an image.

## Related

- [[structure-adding-a-custom-backend-module]] — profile and fragment wiring for image modules
- [[external-api-adapter-pattern]] — the backend side that calls such a service
- [[document-generation-pipeline]] — a pipeline that hands documents to an external converter
- [[karaf-customization-via-fragments]] — passing service URLs as OSGi configuration
- [[osgi-karaf-bundle-architecture]] — the bundle modules these folders sit beside

---
title: Frontend Build and Deployment
description: Maven build modes, module properties, base href and context path, login metadata, MUI license plan and checksum handling of the generated React frontend.
aliases: [frontend maven build, build mode for react, base href wrong path, MUI license key setup, frontend checksum ignore, login metadata frontend]
keywords: [frontend-build-type, quick, skipFrontendModel, ignore-checksums, muiLicensePlan, VITE_MUI_LICENSE_KEY, VITE_API_DEFAULT_BASE_URL, replace-base-href, generator-checksum-ignore, GET_METADATA]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Frontend Build and Deployment

Build modes, module properties, base href handling and MUI licensing of the generated React frontend.

## Maven Build Modes

The generated frontend actor `pom.xml` selects a build strategy with the property `frontend-build-type`:

| Value | Steps |
|-------|-------|
| unset (default, full) | pnpm install, format, build, test |
| `CI` | pnpm install, build, test |
| `quick` | format and `build:reckless` |

Generated `package.json` scripts: `dev`, `build:reckless`, `build`, `preview`, `test:dev`, `test`, `coverage` and `format`. There is no `build:ci` script. `build` runs `tsgo` (type check) before `vite build`. `build:reckless` runs plain `vite build` with no type check.

System properties: `-DskipFrontendModel`, `-DskipPrepareNodeJS`, `-DskipGenerateServices`, `-Dfrontend-build-type=quick` (there is no `-Dquick` property; `quick` is a value of `frontend-build-type`), `-Dlocal` (any value: skips the `replace-base-href` profile, which is active when `local` is not set; the profile is generated only for multi-actor applications), `-Dignore-checksums`.

## Module Properties

Defined in the generated pom: `model-artifactId`, `model-name`, `model-version`, `actor-name`, `node-install-dir` (default `${maven.multiModuleProjectDirectory}/.nodejs`, set in the parent frontend-react pom and inherited by the actor pom), `override-dir` (default `${project.parent.basedir}/generator-overrides`), `muiLicensePlan` (default `community`) and `appVersion` (default `1.0.0`).

Generator template parameters, including `debugPrint`, are set in the `<templateParameters>` element of the `judo-ui-generator-maven-plugin` `generate` configuration. The React template reads `debugPrint` from the template context (`ReactStoredVariableHelper.isDebugPrint`). That context value comes from the `templateVariables` step of `variablePrecedence` (default `projectProperties,templateVariables,propertiesFiles,environmentVariables,systemProperties`), which is the `<templateParameters>` map. No separate `<templateVariables>` element exists. When `debugPrint` is unset it is false.

## Context Path and Base Href

In a multi-actor application each actor frontend is served under the context path `/<model-name>_react/<actor-name>`; a single-actor application is served at its single application path or `/`. The profile `replace-base-href` (active when `local` is not set and the application is not single-actor) rewrites `<base href="/">` in `dist/index.html` to `/<model-name>_react/<actor-name>/` so that assets resolve. `-Dlocal` keeps `<base href="/">`. The backend URL is set with `VITE_API_DEFAULT_BASE_URL` (not `VITE_API_BASE_URL`).

## Login Metadata

For an actor with a `realm` annotation the backend metadata operation (`GET_METADATA`) returns an OpenID descriptor in its `security` list: `issuer`, `authEndpoint`, `tokenEndpoint`, `logoutEndpoint` (from `end_session_endpoint`) and `defaultScopes` (always `email`). The `clientBaseUrl` entry is currently the literal string `"TODO"`; do not rely on it.

## MUI License Plan

The generator parameter `muiLicensePlan` is `community` (default or empty), `pro` or `premium`. Supply it per application through the generator parameters (for example from `secret.env` via `judo.sh`).

- The license key is read at runtime from `VITE_MUI_LICENSE_KEY` (`LicenseInfo.setLicenseKey` in `main.tsx`); `@mui/x-license` is added to `package.json` only for licensed plans.
- Identifiers change: `DataGrid` becomes `DataGridPro`/`DataGridPremium`; the `@mui/x-data-grid` import gets a `-pro`/`-premium` suffix; the date-pickers import gets `-pro` for both licensed plans.
- Gated features: `useInlineColumnFilters=true` is honoured only with a licensed plan (otherwise forced to false); multi-column default sort is generated only on the Pro plan; pinned action column and the `mui-data-grid-pro` theme fragment apply on Pro.
- Without a plan the code is generated for community and Pro features are silently omitted.

## Checksum Handling

A `.generator-checksum-ignore` file (gitignore-style globs) marks files that skip checksum validation and are always regenerated even when manually modified. This differs from `.generator-ignore`, which prevents the file from being written at all. A matching file that differs from its saved checksum is overwritten and the checksum updated instead of failing the build.

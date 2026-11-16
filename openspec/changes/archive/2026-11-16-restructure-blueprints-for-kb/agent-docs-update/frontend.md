# agent-docs/frontend: sweep inventory (80 items)

Each item: id, kind, target, source, status, claim, fact, evidence.

## FR-001 [missing] Other agent-docs topics from knowledge-gaps-report
- target: agent-docs/(general) | src: session:jb-029.json | status: reported-unvalidated
- fact: Topics listed (agent-docs section): binary upload/download two-phase token flow; SYSTEM/non-principal actors exposure and realm; UI model values that break the generator; long-running operations frontend/proxy 503 timeout; creating/upgrading a JUDO project (archetypes, version updater); static navigations and static data; request tracing (exchange id); low-level persistence hooks; API-level tests with ApiClient/Postman; backend CORS filter config; Flutter frontend build (scope-gated).
- evidence: knowledge-gaps-report.md headings lines 117-639 (session 2026-11-09T09:25:04Z)

## FR-002 [missing-how-to] Guest page and guest access mode
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: With `supportGuestAccess` enabled, an unauthenticated user is not redirected to signinRedirect; instead the Auth gate renders a Pandino-overridable guest page. The guest page component is registered as an FC under GUEST_PAGE_INTERFACE_KEY (the constant 'GuestPage', used as the Pandino filter objectClass=GuestPage), typically in the generated registerGuestPage(context) function, and presents a 'Login / Register' button (i18n key judo.guest-page.login-register) that calls signinRedirect().
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/auth/Auth.tsx.hbs:18', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/auth/Auth.tsx.hbs:62', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/custom/default-guest-page-hook-registration.tsx.hbs:13']

## FR-003 [missing-how-to] Binary file upload/download two-phase token flow
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: File upload/download over REST is a two-phase, token-gated protocol: uploadFile first POSTs '<attributePath>/~upload-token' to obtain a token, then POSTs multipart data to the upload path with an X-Token header; downloadFile GETs the download path with ?disposition=inline|attachment plus X-Token and a blob response. The generated fileHandling hook (downloadFile/uploadFile/exportFile/extractFileNameFromToken) wraps this. A developer building custom attachments must understand the token dance and the disposition inline-vs-attachment branch (inline renders in a dialog iframe).
- evidence: ['judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescript-rest-axios/src/main/resources/data-axios/accessServiceImpl.ts.hbs:36', 'judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescript-rest-axios/src/main/resources/data-axios/accessServiceImpl.ts.hbs:64', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/utilities/file-handling.tsx.hbs:54', 'judo-ui-react-templat

## FR-004 [missing-how-to] E2E should drive real UI, API only for access/hidden-menu cases
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The team convention is that e2e tests must navigate through the actual pages and assert visible elements via the browser rather than calling REST endpoints directly; only access-related assertions that verify hidden menu items/authorization shape may remain REST-only. This keeps the UI behaviour (buttons, dialogs, navigation) under test and avoids false-green API-level coverage.
- evidence: ['feat-implemeting_fault_registry_flows : [U] u should call the e2e test through the browser not through the api endpoint u should navigate through the pages and check the elements', 'feat-implemeting_fault_registry_flows : [U] you have to document to use ui based test mostly', 'feat-implemeting_fault_registry_flows : [U] only the access related test which has hidden menu items can be only only']

## FR-005 [missing-how-to] E2E suite methodology: seed from one base dump, test groups derived from it, ~2-minute budget, UI-over-REST with mermaid-model guidance
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: For JUDO E2E suites, create the DB once from a single base dump and derive all test groups from that dump (no new dumps per test), keeping each test run within ~2 minutes; use a cloneable PostgreSQL for quick test purposes. Prefer UI tests (Playwright) over REST tests whenever an assertion targets a rendered/frontend fact (e.g. a control's presence/absence), keeping REST only for authorization-vs-validation distinctions the browser cannot see, and use the generated mermaid model (via judo-cli) as the source of truth for what appears on each view/table/form screen.
- evidence: ['fix-fault-registry-flow : [U] please use a base dump, and create test groups form that dump and check the test on them, base dump no new dump creation, and should the test run within 2 minutes', 'fix-fault-registry-flow : [U] When u plan ui and rest test check the generated mermaid model with judo cli which can extract the whole model especialy the view table, and form pages', 'fix-fault-registr

## FR-006 [missing-topic] UI element fully-qualified-name (FQN) conventions
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: FQN resolution rules for the UI model are non-uniform: an Application's FQN is its simple name; a Theme is <AppName>::Theme; a Frame is <containerFQN>::Frame; MimeType uses type/subType with a '/' separator; other NamedElements use a :: hierarchy; elements without a usable name fall back to the XMI URI fragment. These rules are implemented in UiFqnResolverImpl and drive the CLI's model type 'ui' and FqnCache-backed resolution.
- evidence: ['judo-meta-ui@7bdc5ac:model/src/main/java/hu/blackbelt/judo/meta/ui/cli/UiFqnResolverImpl.java:125', 'judo-meta-ui@7bdc5ac:model/src/main/java/hu/blackbelt/judo/meta/ui/cli/UiFqnResolverImpl.java:136', 'judo-meta-ui@7bdc5ac:model/src/main/java/hu/blackbelt/judo/meta/ui/cli/UiFqnResolverImpl.java:164', 'judo-meta-ui@7bdc5ac:openspec/specs/runtime/osgi-and-cli/spec.md:135']

## FR-007 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:139
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: String helper capitalize: 'hello' becomes 'Hello'.
- fact: No capitalize helper exists. The equivalent is firstToUpperCase(String).
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:139

## FR-008 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:140
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: String helper camelToSnake: 'myVar' becomes 'my_var'.
- fact: No camelToSnake helper exists. The helper is camelCaseToSnakeCase, which returns UPPER_UNDERSCORE, so 'myVar' becomes 'MY_VAR'.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:140

## FR-009 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:36
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: The camel-to-snake example uses CaseFormat.LOWER_UNDERSCORE and returns lowercase snake_case.
- fact: StringHelper.camelCaseToSnakeCase uses CaseFormat.UPPER_UNDERSCORE.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:36

## FR-010 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:146
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: URI helpers pathOf and schemeOf exist.
- fact: Neither pathOf nor schemeOf exists. UriHelper provides calculateRelativeURI, concatUri and lastPart.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:146

## FR-011 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:120
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Collection<Class<?>> helpers = TemplateHelperFinder.collectHelpers(packageName, classLoader).
- fact: collectHelpers returns Collection<String> (class names). The Class-returning method is collectHelpersAsClass.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:120

## FR-012 [wrong-fact] src/main/resources/agent-docs/components/template-system.md:94
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ChainedURLTemplateLoader.createFromURIs(Arrays.asList(overrideUri, baseUri), 'templates').
- fact: createFromURIs takes only Collection<URI>; the second 'templates' argument does not exist.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/template-system.md:94

## FR-013 [wrong-fact] src/main/resources/agent-docs/components/generator-ignore.md:73
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: A '!' prefix in .generator-ignore negates a pattern, so '!generated/important.txt' keeps the file.
- fact: GeneratorIgnore has no negation handling. Each line is passed unchanged to FileSystems.getPathMatcher('glob:' + line) and the results are OR
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/generator-ignore.md:73

## FR-014 [wrong-fact] src/main/resources/agent-docs/components/generator-ignore.md:96
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Patterns from deeper directories take precedence over patterns from higher levels.
- fact: shouldExcludeFile returns true if any pattern from any level matches. It walks upward and stops at the first match, but there is no preceden
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/generator-ignore.md:96

## FR-015 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:514
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: Password checks are independent if-statements that each assign errors.password; the last failing check overwrites earlier messages, so a sho
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:514

## FR-016 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:133
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: Holiday check formats the date with date.toISOString().split('T')[0], which is the UTC calendar date, while the weekend check uses local dat
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:133

## FR-017 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:401
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: checkTitleAvailability is a lodash debounce around an async call; lodash debounce returns the result of the last invocation, so the first ca
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:401

## FR-018 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/ui-hooks.md.hbs:478
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: The menu reorder example calls menuItems.sort(...), which mutates the array passed in by the framework rather than returning a new array.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/ui-hooks.md.hbs:478

## FR-019 [mention-only] Generated table state persistence keys and uniqueId uniqueness
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: LazyTable and EagerTable persist grid state in sessionStorage under structured keys built from the table's uniqueId: `${uniqueId}-sortModel`, `${uniqueId}-filterModel`, `${uniqueId}-filters`, `${uniqueId}-rowsPerPage`, and (on the MUI Pro build) `${uniqueId}-columnState`. Because the keys are derived only from uniqueId, uniqueId must be unique per table or two tables will read/write each other's state.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/components/table/LazyTable.tsx.hbs:72', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/components/table/EagerTable.tsx.hbs:155']

## FR-020 [mention-only] Operation fault dialog API
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: `useFaultDialog()` returns `(faultObjectKey: string, payload: any) => void`, which opens an OperationFaultDialog in the StackableDialogProvider and renders the business-fault payload as translated key/value pairs. Each payload key is shown with label `t('faults.<faultObjectKey>.<key>')` and data-testid `faults.<faultObjectKey>.<key>`. Relatedly, useCRUDDialog builds fault messages from `error.response.data` keys as `faults.<faultPrefix>.<object>.<attribute>`.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/components/dialog/OperationFaultDialog.tsx.hbs:16', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/components/dialog/OperationFaultDialog.tsx.hbs:65', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/hooks/useCRUDDialog.tsx.hbs:159']

## FR-021 [mention-only] Per-component MUI theme override fragments
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The generated theme (index.tsx.hbs) is assembled from a fixed set of per-component override fragments: actor/src/theme/index.ts.mui-app-bar/mui-autocomplete/mui-button/mui-card/mui-dialog/mui-data-grid[/pro]/mui-form-control/mui-input-base/mui-list/mui-paper/mui-select/mui-tab/mui-text-field/mui-tooltip.fragment.hbs, plus palette.ts.extra-attributes/extra-imports/extra-palette-attributes.fragment.hbs and theme-options.fragment.hbs. Each is overridden by creating a same-named file in the application's actor/src/theme/. The catalog describes the general Handlebars fragment override mechanism but does not enumerate these specific theme fragment names and their defaults.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/theme/index.ts.mui-app-bar.fragment.hbs:2', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/theme/index.ts.mui-button.fragment.hbs:10', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/theme/palette.ts.extra-attributes.fragment.hbs:1', 'judo-ui-react-template@af315252

## FR-022 [mention-only] Frontend hook files are generated only when the hook is set in the model; the src/custom folder is gitignored so .generator-ignore entries are not needed for hooks
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The frontend generator emits a hook file only when the corresponding frontend hook/action flag is set in the model (e.g. generateActionsHook); without the model flag there is no scaffold to customize. Custom hook code lives in src/custom/, which is gitignored, so hook customizations survive regeneration and do NOT need .generator-ignore entries (unlike other overrides).
- evidence: ["judo-cli-sessions__2026-09-15T07-11 : 'D5: The framework generates the file for the frontend hooks, if the frontend hook is set in the model. The whole custom folder in the frontend project is gitignore. Generator ignore not needed here'", "judo-cli-sessions__2026-09-17T10-21 : '0.3 — generateActionsHook = true on the two forms. Which two form?'"]

## FR-023 [missing] Frontend 422 fault dialog behaviour
- target: agent-docs/frontend | src: session:jb-031.json | status: validated
- claim: No docs of how modeled faults render.
- fact: error-handling.ts.hbs:136-139: 422 detected by status only (isErrorOperationFault :228-230); the X-Fault header is never read. It takes only the first key of the body (Object.keys(data)[0]) and opens OperationFaultDialog (title judo.error.error, body judo.error.business-fault). Each detail is translated as t('faults.<faultObjectKey>.<attr>', {defaultValue: key}). Batch variant in useCRUDDialog.tsx.hbs:155-170 uses faults.<faultPrefix>.<key>.<attr>. Other statuses: 500 internal-server-error toast; 401 clears storage and reloads (axiosInterceptor.ts.hbs:65-68) so the toast is mostly unseen; 403, 404 toasts; other statuses use error.unknown. A custom hook custom/default-error-handler-interceptor.ts.hbs runs first (not reviewed).
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore frontend

## FR-024 [missing] Frontend: location-less 400 validation errors are dropped/generic; custom 422 override
- target: agent-docs/frontend | src: session:jb-032.json | status: validated
- claim: n/a
- fact: Default handler src/utilities/error-handling.ts: 500 toast judo.error.internal-server-error; 422 -> openFaultDialog(key,data[key]) rendering faults.<prefix>.<faultObjectKey>.<attribute> i18n keys (defaultValue = attribute name); 400 -> generic judo.error.validation-failed toast, field map only if errorList[0].location exists (:165). Location-less items fall under key '' so no field shows them; custom interceptor path (operationValidationFeedback.ts:59,100) filters them. Only 3 codes translated by default in en-US (REQUIRED_GROUP_MUST_HAVE_AT_LEAST_ONE_ROW, REQUIRED_FIELD_MISSING, VALUE_NOT_ALLOWED), other codes fall back to raw code string (error-handling.ts:206-210). Rackinspect overrides via src/custom/hooks/register-error-handler-interceptor.ts (registered in custom/application-customizer.tsx:240): intercepts ALL 422s and shows 3s snack with data[firstKey].message, bypassing fault dialog. useCRUDDialog.tsx:155-170 still renders faults.* directly.
- evidence: Rackinspect frontend rackinspect__services__generic_user/src/utilities/error-handling.ts:125-242

## FR-025 [missing] Generated frontend error handling matrix (400/422/401/403/404/500)
- target: agent-docs/frontend | src: session:sweep-012.json | status: validated
- claim: (not documented)
- fact: utilities/error-handling.ts.hbs useErrorHandler: 400 -> toast judo.error.validation-failed + inline errors only if errorList[0].location exists; 422 -> only first key of body, opens OperationFaultDialog (title judo.error.error, per-field text faults.<fqn>.<attr> default raw attr); detection by status only, X-Fault header never read; 401 clears storage and reloads (toast never seen); 403/404/500 toasts; else error.unknown. Fault i18n key faults.<faultPrefix>.<faultObjectKey>.<attribute>. Only 3 validation codes translated by default; others fall back to raw code.
- evidence: judo-ui-react actor/src/utilities/error-handling.ts.hbs:72-230; OperationFaultDialog.tsx.hbs:16-65

## FR-026 [missing-how-to] GET_METADATA OpenID security descriptor for frontend login
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The backend's GET_METADATA operation builds, for an actor type carrying a 'realm' extension annotation, an OpenID/OAuth security descriptor returned as the 'security' list. OpenID config keys are mapped issuer->issuer, auth_endpoint->authEndpoint, token_endpoint->tokenEndpoint, end_session_endpoint->logoutEndpoint; defaultScopes is always 'email'; and the 'clientBaseUrl' entry is currently the literal string "TODO".
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/GetMetadataCall.java:47', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/GetMetadataCall.java:76', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/co

## FR-027 [missing-how-to] Frontend context path and multi-actor routing / base href
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: Each actor's React frontend is hosted at an OSGi Web-ContextPath of /<model-name><frontend postfix>/<actor-name> for multi-actor apps (or singleApplicationPath / '/' for a single-actor app). A replace-base-href Maven profile (active when the property local is not set and the app is not single-actor) rewrites <base href="/"> in dist/index.html to /<model-name>_react/<actor-name>/, so assets resolve correctly under the context path; passing -Dlocal keeps base href='/'. The backend URL must be set via VITE_API_DEFAULT_BASE_URL.
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/frontend-react/actor/pom.xml.hbs:37', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/frontend-react/actor/pom.xml.hbs:431', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/res

## FR-028 [missing-how-to] Frontend Maven build modes and module properties (frontend-build-type, muiLicensePlan, override-dir)
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The generated React frontend actor POM selects a build strategy via `frontend-build-type`: default `full` (pnpm install/format/build/test), `CI` (install/build/test), `quick` (format + build:reckless). Key properties are `model-artifactId`, `model-name`, `model-version`, `actor` (fully-qualified), `actor-name`, `node-install-dir` (default `${project.parent.basedir}/.nodejs`), `override-dir` (client override location, default `${project.parent.basedir}/generator-overrides`), `muiLicensePlan` (default `community`) and `appVersion` (default `1.0.0`). System properties control the build: `-DskipFrontendModel`, `-DskipPrepareNodeJS`, `-DskipGenerateServices`, `-Dquick`, `-Dlocal`.
- evidence: ['judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-application/src/main/resources/frontend-react/actor/pom.xml.hbs:332', 'judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-application/src/main/resources/frontend-react/actor/pom.xml.properties-definition.fragment.hbs:8', 'judo-jsl-fullstack-karaf-project-template@d

## FR-029 [missing-how-to] Sub-theme hook registration API
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: A named sub-theme is registered by a generated `register<SubTheme>SubThemeHook(context)` which calls `context.registerService(SUB_THEME_HOOK_INTERFACE_KEY, fn, { name: '<toSafeCamelCase subTheme>' })`. The registered function receives `(parentTheme: Theme, data?: any)` and returns `{ components: {...} }` MUI style overrides (the generated sample overrides MuiPaper styleOverrides.root). The sub-theme name is derived via toSafeCamelCase.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/custom/sub-theme-hook-registration.tsx.hbs:12', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/custom/sub-theme-hook-registration.tsx.hbs:17']

## FR-030 [missing-how-to] Extra routes extension point
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The generated `src/extra-routes.tsx` exports an `extraRoutes: Array<{ path: string; element: ReactElement; exact?: boolean }>` array that the generated routes.tsx prepends to the generated routes. It is generated empty and is the supported way to add custom React Router routes without editing generated routing files.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/extra-routes.tsx.hbs:5']

## FR-031 [missing-how-to] Renaming a model operation propagates to generated frontend (duplicate updateAction, missing custom hook path)
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: Renaming an operation in the model regenerates frontend action/container files and custom hook scaffolds; a rename can produce duplicate `updateAction` identifiers in generated `types.ts` and orphan `Cannot find module '~/dialogs/...CreateDefectTicketInputFormActionsHook'` imports, and old `.default` scaffolds remain until regenerated with `-i`. After a rename you must regenerate with the build recipe (`./judo.sh build -i`) and check every generated/custom reference to the old name.
- evidence: ['judo-cli-sessions__2026-09-28T18-23 : "error TS2300: Duplicate identifier \'updateAction\'" / "error TS2307: Cannot find module \'~/dialogs/Services/Partner_service/Partner/.../CreateDefectTicket/Input/Form/customization\'"', 'judo-cli-sessions__2026-09-28T18-23 : "Okay, rename the update, because i want it in the container. So please rename it and fix all the regressions. First update the spec 

## FR-032 [missing-how-to] Misleading UiValidationException "All constraints have been satisfied" gives zero diagnostics; binary-search UI layout groups
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: A frontend model/build failure can surface as `UiValidationException: All constraints have been satisfied` — an ERROR that reports no actual failed constraint, forcing a slow bisect. The working technique is to remove all UI layout mutations, restore a passing build, then re-add them one group at a time (rebuilding after each) to isolate the culprit; several true root causes (invalid widget, TabRef columns, ActionGroup-wrapped OperationForms) were hidden behind this opaque message.
- evidence: ['rackinspect-sessions (2026-05-16T23:34Z) : ## How I solved "All constraints have been satisfied" ... The error message `UiValidationException: All constraints have been satisfied` was misleading — it appeared as an ERROR but gave zero diagnostic detail ... binary search by group ... I removed them all to restore a passing build. Then I re-added them one group at a time, rebuilding after each to 

## FR-033 [missing-how-to] UI widget/layout values that break the generator (SWITCH widget, TabRef columns on unmapped input TOs, ActionGroup-wrapped OperationForms)
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: Several ESM UI-layer values silently break frontend generation: `booleanWidget: "SWITCH"` does not exist (the Handlebars generator has no `switch.hbs` partial, so use `CHECKBOX`/`COMBO`); `TabularReferenceField` columns that reference attributes from an external TO/namespace on an unmapped input TO break the build; wrapping `OperationForm`s in an `ActionGroup` on a view can fail UI validation while placing the OperationForms directly on the view passes; and new TO attributes/operations are not auto-placed on forms/views — each must be explicitly added as a `DataField`/`OperationForm` before the generator renders a control.
- evidence: ['rackinspect-sessions (2026-05-16T19:51Z) : ## Session Learnings ... 6. New TO attributes/operations are NOT auto-placed on form/view layouts ... 7. `booleanWidget: "SWITCH"` does NOT exist — the generator fails with "partial \'switch.hbs\' could not be found". Use "CHECKBOX" or "COMBO". 8. TabularReferenceField columns on unmapped input TOs break the build — columns referencing attributes from e

## FR-034 [missing-pattern] Authoring generator templates: YAML descriptor fields and template context variables
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: Generator templates are driven by a <type>.yaml descriptor with per-template fields: name, templateName, pathExpression (SpEL output path), applicationBased (run once per application vs once per factory result), conditionExpression (SpEL skip condition), factoryExpression (SpEL iteration), copy, exclude, permission (POSIX), and templateContext. Template context variables exposed to Handlebars/SpringEL are #self, #application, #applications, #model, #template, and #addDebugToTemplate (set when the -DtemplateDebug JVM property is present). Overrides layer as: same-name template with a new templateName/pathExpression replaces it, a <name>.override.hbs file decorates it (and can include the original as a partial), and exclude: true removes it.
- evidence: ['judo-meta-ui@7bdc5ac:openspec/specs/generator/template-engine/spec.md:53', 'judo-meta-ui@7bdc5ac:openspec/specs/generator/template-engine/spec.md:83', 'judo-meta-ui@7bdc5ac:openspec/specs/generator/template-engine/spec.md:130', 'judo-meta-ui@7bdc5ac:openspec/specs/generator/template-engine/spec.md:137', 'judo-meta-ui@7bdc5ac:generator-maven-plugin/README.md:106', 'judo-meta-ui@7bdc5ac:generator-

## FR-035 [missing-pattern] Menu actions hook objectClass gotcha
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The menu-actions customization hook is registered under the OSGi objectClass value 'MENU_ACTIONS_HOOK' — without the 'Hook' suffix used by every other hook key (CustomHeroPropsHook, CustomLogoPropsHook, FooterTextHook, MenuItemsCustomizerHook). Its interface key constant is MENU_ACTIONS_HOOK_INTERFACE_KEY from ~/layout/.../menuCustomization, and registered handlers return a MenuPageActions object with an optional handler per navigation-controller action.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/Drawer/DrawerContent/Navigation/menuCustomization.ts.hbs:6', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/Drawer/DrawerContent/Navigation/menuTypes.ts.hbs:10']

## FR-036 [missing-pattern] Frontend generated TS breaks when model transfer objects are retargeted/added: stale custom-hook import paths and type drift
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: Adding or retargeting transfer objects in the model regenerates the frontend TypeScript surface, and custom hooks that import from generated dialog/page customization modules break with TS2307 'Cannot find module' when the path is removed or renamed (e.g. ~/dialogs/Services/.../RelationViewPage/hooks). Also, retargeting a shared TO to a lean projection changes its Stored type (e.g. Servicesai_serviceRackStored vs Servicesrack_serviceRackStored) and the frontend rejects it for missing properties (active, brand, rackType). Customizations that live in the wrong generated location must be moved, and retargeting a TO used by the UI has frontend-wide type consequences.
- evidence: ['<judo-cli-sessions__sessions__2026-09-19T09-16-55-032Z_01a0b8f4-5377-74f2-a82f-c8406ca07386.jsonl> : "error TS2307: Cannot find module \'~/dialogs/Services/Dimension_service/DimensionTemplateParameter/Unit/RelationViewPage/hooks\' or its corresponding type declarations."', '<judo-cli-sessions__sessions__2026-09-19T22-20-11-003Z_01a0bbc1-6d7a-72a8-b2a9-97e634e425e5.jsonl> : "Type \'Servicesai_ser

## FR-037 [missing-pattern] Frontend features must be modeled as ESM UI elements, not implemented as whole custom components
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: To add a new field/column/operation to the UI, the proper approach is to model the UI parts in the ESM model (add the element to the View/Form/Table transfer objects, with the canonical <TO>View/Form/Table naming) and then customize behavior via Pandino hooks/overrides — not to implement the whole feature as a custom frontend component replacing generated code. Backend operations may be custom, but the frontend must be model-driven.
- evidence: ['rackinspect 2026-05-07T13:13:41 : [U] u have to add to the models UI parts to element do you know that? U have the opportunity to create hooks and overrides on the frontend, check the agents_docs related parts', 'rackinspect 2026-05-13T09:11:16 : [U] frontend should be added by model element not implemented as whole custom element, check how to you add to the view, form, table the new elements .

## FR-038 [missing-topic] .generator-checksum-ignore: forced regeneration of manually modified files
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The generator supports a .generator-checksum-ignore file whose .gitignore-style globs mark files that skip checksum validation and are always regenerated, even when manually modified. This is distinct from .generator-ignore (which prevents files from being written/indexed/deleted at all). When a matching file differs from its saved checksum, it is overwritten and its checksum updated instead of raising the manual-modification error.
- evidence: ['judo-meta-ui@7bdc5ac:openspec/specs/generator/checksum-and-sync/spec.md:56', 'judo-meta-ui@7bdc5ac:openspec/specs/generator/checksum-and-sync/spec.md:118', 'judo-meta-ui@7bdc5ac:openspec/specs/template-enhancements/spec.md:52']

## FR-039 [missing-topic] MUI license plan, key and feature gating
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The React generator is parameterised by the `muiLicensePlan` template parameter (empty/community, pro, premium). The MUI license key is read at runtime from the Vite env var VITE_MUI_LICENSE_KEY (LicenseInfo.setLicenseKey in main.tsx); the `@mui/x-license` runtime dependency is added to package.json only when a licensed plan is set. The plan also changes generated identifiers: the DataGrid component becomes DataGridPro/DataGridPremium, the @mui/x-data-grid import path gets a -pro/-premium suffix, and the date-pickers import gets a -pro suffix for both pro and premium. Crucially, features are gated: useInlineColumnFilters=true is honoured only when a licensed plan is set (otherwise forced false), and multi-column default sort (getDefaultSortParamsForTable) is emitted only on the Pro plan.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/ReactStoredVariableHelper.java:66', 'judo-ui-react-template@af315252:judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/ReactStoredVariableHelper.java:84', 'judo-ui-react-template@af315252:judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/UiTableHelper.java:275', 'judo-ui

## FR-040 [missing-topic] MUI X license tier configuration
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The generated React frontend gates licensing-dependent behavior on the isMUILicensed / isMUILicensePlanPro flags and reads the MUI X license from the VITE_MUI_LICENSE_KEY environment variable at build time (LicenseInfo.setLicenseKey). A developer using commercial MUI X DataGrid Pro/Premium features must set VITE_MUI_LICENSE_KEY and configure the license plan (muiLicensePlan) in the generator parameters; the plan also controls which package suffix and DataGridPro styles are emitted. None of this configuration surface is documented in the catalog.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/main.tsx.hbs:37', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/theme/index.ts.mui-data-grid-pro.fragment.hbs:2', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/vite-env.d.ts.hbs:4', 'judo-ui-react-template@af315252:judo-ui-react-itest/ActionGroupTestPro/pom.xml:2

## FR-041 [missing-topic] Multi-application switcher and alternative-app navigation
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The generated app supports switching between alternative applications: ProfilePopup shows an application switcher when otherApplicationsAvailable is true, driven by useApplicationSelector(); changeApplication(key) clears security storage and does a full page navigation to origin + '/' + key, and generateAlternativeApplications builds the key-to-display-name map from translation keys ('applications.<simpleName>'). A developer building a multi-app deployment (e.g. different realms/products on one origin) needs this contract.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/ProfilePopup/index.tsx.hbs:47', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/utilities/application/change-application.ts.hbs:9', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/utilities/application/generate-alternative-applications.ts.hbs:8']

## FR-042 [missing-topic] useNavigationConfirmation generated hook
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: A generated hook useNavigationConfirmation.ts is emitted (per ui-react.yaml) to gate navigation away from edited state. The catalog never mentions this hook or its purpose, so developers do not know it exists or how to leverage it for unsaved-changes confirmation.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/ui-react.yaml:251', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/ui-react.yaml:251']

## FR-043 [missing-topic] Frontend service-operation timeout drops long operations with 503
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: Operations that run longer than roughly 30 s get dropped by the frontend service layer with HTTP 503 even though the backend returns the response correctly for big/long operations. The request timeout is configured in the React frontend service layer, not the backend; backend long-running operation responses must be paired with a matching frontend timeout (or async/job handling) so the client does not abort.
- evidence: ['rackinspect 2026-06-09T08:11 : [U] check frontend services timeout application/react-frontend check there is any timeout for the service operations (backend add back the response for bigger time taken operation correcrly, but frontend sent 503 )', 'rackinspect 2026-06-09T08:11 : [U] so if an operation roun for 30 second its dropped?']

## FR-044 [missing-topic] Enabling the MUI X Pro license in the generated React frontend
- target: agent-docs/frontend | src: gap-mining | status: mined
- fact: The JUDO React generator reads a `muiLicensePlan` generator property (community|pro|premium) that is resolved by `ReactStoredVariableHelper.isMUILicensed()/isMUILicensePlanPro()` and drives template branches such as pinned-columns in LazyTable (`{{# if isMUILicensePlanPro }} initialState={ { pinnedColumns: { right: ['actions'] } } }`). The value is injected from the generator pom (pom.xml.hbs `muiLicensePlan` property / properties-definition fragment) and can be supplied per-app through `judo.sh` from a `secret.env`, with the CLI build receiving the key the same way rail-cargo does. Without setting it, code is generated under the community plan and Pro features are silently omitted.
- evidence: ['rackinspect-20261102 11:35 : [U] There is the rail cargo project projects/rail-cargo project use pro mui license key, list what will change if we set this key in our application', "rackinspect-20261102 11:35 : [DIG>] {{# if isMUILicensePlanPro }} ⏎ initialState={ { pinnedColumns: { right: ['actions'] } } } ⏎ {{/ if }}", 'rackinspect-20261102 11:35 : [DIG>] <muiLicensePlan>{{# if muiLicensePlan }

## FR-045 [wrong-fact] frontend README: generated output location
- target: agent-docs/frontend | src: session:jb-007.json | status: reported-unvalidated
- claim: Generated output is under src/generated/.
- fact: React template writes generated files to src/containers/... (ui-react.yaml:827); typescript-rest template writes to data-service/ (ui-typescript-rest.yaml:4-16).
- evidence: judo-ui-react-template@ad0848bc:ui-react.yaml:827 (finding FE-001)

## FR-046 [wrong-fact] frontend hooks: application-customizer file
- target: agent-docs/frontend | src: session:jb-007.json | status: reported-unvalidated
- claim: application-customizer.tsx.default is a generated .default file you edit.
- fact: It is generated as plain src/custom/application-customizer.tsx (ui-react.yaml:289-291).
- evidence: judo-ui-react-template@ad0848bc:ui-react.yaml:289 (FE-003)

## FR-047 [wrong-fact] frontend action hooks: interface key names
- target: agent-docs/frontend | src: session:jb-007.json | status: validated
- claim: PAGE_ACTION_HOOK_INTERFACE_KEY (and in advanced-patterns ERROR_HANDLER_HOOK_INTERFACE_KEY, BLUR_ACTION_HOOK_INTERFACE_KEY, POST_REFRESH_ACTION_HOOK_INTERFACE_KEY, CUSTOM_COMPONENT_HOOK_INTERFACE_KEY imported from @judo/web-react).
- fact: None exist. Real key is per-page <PAGE>_ACTIONS_HOOK_INTERFACE_KEY (default-page-hook-registration.ts.hbs:33); error handler key is ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY in utilities/error-handling.ts.hbs; the package @judo/web-react is not in the template and absent from all judo-ng. Verifier: FE-008 only partly right.
- evidence: judo-ui-react-template@ad0848bc (FE-008, FE-010, FE-011); absence re-grepped across all judo-ng

## FR-048 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md.hbs:393
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: generateActionsHook link target hooks/action-hooks.md#generated-action-hooks
- fact: action-hooks.md.hbs has no heading that produces the anchor generated-action-hooks; its ## headings are Container Actions, Enumeration Filte
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md.hbs:393

## FR-049 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md.hbs:394
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: generateVisualPropertiesHook link target hooks/ui-hooks.md#visual-property-hooks
- fact: ui-hooks.md.hbs has no visual-property-hooks heading (its sections are AppBar Extra Components, Hero and Logo Customization, Footer Text, Me
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md.hbs:394

## FR-050 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/data-hooks.md.hbs:231
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: Developers do not create a useViewData hook; view data comes from hook parameters
- fact: The same file then imports useViewData from '~/custom/hooks/useViewData' (line 293, 327, 358) and calls useViewData('entityView') with a str
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/data-hooks.md.hbs:231

## FR-051 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/action-hooks.md.hbs:381
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: Container hook calls context.refresh() (also at line 403)
- fact: data-hooks.md.hbs:271 documents the refresh API as context.actions.refresh(). The two agent docs disagree on the refresh API; the generated 
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/action-hooks.md.hbs:381

## FR-052 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/action-hooks.md.hbs:263
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: debounce(async fn, 300) wrapped as debouncedSearch; caller does 'const result = await debouncedSearch(searchText); return result.data;'
- fact: lodash debounce returns the result of the last invocation and undefined for calls that are still pending, so the awaited value is usually un
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/action-hooks.md.hbs:263

## FR-053 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:690
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: Complete example destructures the async result directly: const { exists } = await checkTitleAvailability(title).
- fact: Earlier examples in the same file read the response as result.data?.exists (line 401), i.e. the response shape is { data: { exists } }; the 
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:690

## FR-054 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/ui-hooks.md.hbs:609
- target: agent-docs/frontend | src: judo-ng-read | status: validated
- claim: APPBAR_COMPONENTS_INTERFACE_KEY is used with context.registerService to register AppBar components.
- fact: The symbol is not imported in the example (the imports at lines 597 and 603 do not include it) and is not defined anywhere in the template w
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/ui-hooks.md.hbs:609

## FR-055 [wrong-fact] # Edit the .default file directly
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: application-customizer.tsx.default is generated and must be edited (copied/renamed to remove .default)
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/ui-react.yaml:289-291 (src/custom/application-customizer.tsx is generated as a plain file with no .default variant)

## FR-056 [wrong-fact] ## Common Template Patterns
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: Table: hooks/*.tsx.default (custom hook implementations) and theme/*.ts.default (Usually rename)
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/ui-react.yaml:697-713 (src/theme/palette.ts, typography.ts, table-row-highlighting.ts are plain files); ui-react.yaml:311 (hook registrations are src/custom/hooks/pages/register<Page>ActionsHook.ts.default)

## FR-057 [wrong-fact] # Step 3: Create custom hook
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: Custom hook file src/custom/hooks/tableRowHighlighting.tsx (also listed in .generator-ignore examples)
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/ui-react.yaml:709 (generated path is src/theme/table-row-highlighting.ts); actor/src/theme/table-row-highlighting.ts.hbs:4 (TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY)

## FR-058 [wrong-fact] ### Registration
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: import { CONTAINER_HOOK_INTERFACE_KEY } from '~/generated' (container action hook key)
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/custom/default-container-hook-registration.ts.hbs:6-7,23 (key is <CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY, imported from ~/containers/<path>/customization)

## FR-059 [wrong-fact] ### Registration
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: import { PAGE_ACTION_HOOK_INTERFACE_KEY } from '~/generated' (page actions)
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/custom/default-page-hook-registration.ts.hbs:6,33 (key is <PAGE>_ACTIONS_HOOK_INTERFACE_KEY, generated per page); no literal PAGE_ACTION_HOOK_INTERFACE_KEY in the template

## FR-060 [wrong-fact] ### Basic Implementation
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: import { ViewEntityFormContainerHook } from '~/generated'
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/containers/customization.ts.hbs:22 (generated type <Container>ContainerHook); default-container-hook-registration.ts.hbs:7 (imported from ~/containers/<path>/customization)

## FR-061 [wrong-fact] ### Registration
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: import { CONTAINER_HOOK_INTERFACE_KEY } from '~/generated'
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/custom/default-container-hook-registration.ts.hbs:6-7,23

## FR-062 [wrong-fact] ### Registration
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: import { MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY } from '~/generated'
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/layout/Drawer/DrawerContent/Navigation/index.tsx.hbs:23 (key is defined here, value 'MenuItemsCustomizerHook')

## FR-063 [wrong-fact] ## Common Template Patterns
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: 'Keep .default' guidance for pages/*-hook-registration.tsx.default
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/ui-react.yaml:311,319,327,351,360 (page/dialog/container registrations live under src/custom/hooks/{pages,dialogs,containers}/register*.ts.default)

## FR-064 [wrong-fact] ## Menu Manipulation
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: Menu Manipulation section never mentions registerMenuActionsHook / MENU_ACTIONS_HOOK_INTERFACE_KEY
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/custom/menu-hook-registration.ts.hbs:24-25 (registerMenuActionsHook); actor/src/layout/Drawer/DrawerContent/Navigation/menuCustomization.ts.hbs:4 (MENU_ACTIONS_HOOK_INTERFACE_KEY)

## FR-065 [wrong-fact] (see doc)
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: No coverage of guest page customization (registerGuestPage)
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/custom/default-guest-page-hook-registration.tsx.hbs:12-13 (registerGuestPage registers GUEST_PAGE_INTERFACE_KEY); actor/src/auth/Auth.tsx.hbs:18,62

## FR-066 [wrong-fact] ### 2. UI Hooks
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: Hook categories do not mention sub-theme hooks
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/custom/sub-theme-hook-registration.tsx.hbs:11-12; ui-react.yaml:368 (src/custom/hooks/sub-themes/register<Name>SubThemeHook.tsx.default); actor/src/theme/SubThemeWrapper.tsx.hbs

## FR-067 [wrong-fact] (see doc)
- target: agent-docs/frontend | src: agent-docs-review:frontend.json | status: reported
- claim: Cards container configuration hook (CardsContainerConfigHook) not documented
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/custom/default-cards-config-hook-registration.tsx.hbs:27-28; ui-react.yaml:351

## FR-068 [wrong-fact] ### 2. judo-ui-react-template
- target: agent-docs/frontend/README.md | src: agent-docs-review:frontend.json | status: reported
- claim: src/generated/pages/*.tsx, src/generated/models/*.ts, src/generated/services/*.ts, src/generated/data-axios/*.ts listed as generated output
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/ui-react.yaml:827 (React containers generated to src/containers/...); no pathExpression starts with src/generated; typescript-rest: judo-ui-typescript-rest-template@b4912df:judo-ui-typescript-rest-service/src/main/resources/ui-typescript-rest.yaml:4-16 (output is data-service/*.ts)

## FR-069 [wrong-fact] # Ignore specific hooks
- target: agent-docs/frontend/README.md | src: agent-docs-review:frontend.json | status: reported
- claim: src/custom/hooks/usePrincipal.tsx and src/custom/hooks/useCustomAuth.tsx listed as customizable hook files
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/auth/principal-context.tsx.hbs:66 (usePrincipal is generated in auth/, not a customizable src/custom/hooks file); useCustomAuth not defined anywhere in the template

## FR-070 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:1294
- target: agent-docs/frontend/advanced-patterns.md | src: judo-ng-read | status: validated
- claim: useInlineCreateDialog defines DialogComponent as a component inside the hook body. Each render creates a new component type, so React remoun
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:1294

## FR-071 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:786
- target: agent-docs/frontend/advanced-patterns.md | src: judo-ng-read | status: validated
- claim: The DateInput example uses IMask.MaskedRange, but the only import in the example is 'import { IMaskInput } from react-imask' (line 681), so 
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:786

## FR-072 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:1901
- target: agent-docs/frontend/advanced-patterns.md | src: judo-ng-read | status: validated
- claim: Configuration example reads baseUrl from import.meta.env.VITE_API_BASE_URL (fallback '/api').
- fact: The frontend env var documented everywhere else is VITE_API_DEFAULT_BASE_URL (required). VITE_API_BASE_URL is not documented as a variable.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:1901

## FR-073 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:1130
- target: agent-docs/frontend/advanced-patterns.md | src: judo-ng-read | status: validated
- claim: postRefresh example maps server validation messages with result.field.
- fact: The validation result shape defined in the same document is ValidationResult { location, code, message }; there is no field property.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/advanced-patterns.md.hbs:1130

## FR-074 [wrong-fact] #### Hook Registration
- target: agent-docs/frontend/advanced-patterns.md | src: agent-docs-review:frontend.json | status: reported
- claim: import { ERROR_HANDLER_HOOK_INTERFACE_KEY } from '@judo/web-react'; error interceptor hook
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/utilities/error-handling.ts.hbs:50 (ErrorHandlerInterceptorHook); actor/src/custom/default-error-handler-interceptor.ts.hbs:5,10-11 (ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY, registerErrorHandlerInterceptorHook)

## FR-075 [wrong-fact] #### Registration
- target: agent-docs/frontend/advanced-patterns.md | src: agent-docs-review:frontend.json | status: reported
- claim: BLUR_ACTION_HOOK_INTERFACE_KEY, POST_REFRESH_ACTION_HOOK_INTERFACE_KEY, CUSTOM_COMPONENT_HOOK_INTERFACE_KEY imported from '@judo/web-react'
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/(no definition of these constants or a '@judo/web-react' package in judo-ui-react-template; rg -w finds none)

## FR-076 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/development-workflow.md.hbs:39
- target: agent-docs/frontend/development-workflow.md | src: judo-ng-read | status: validated
- claim: If you only need to clear generator caches, use ./judo.sh clean instead.
- fact: judo.sh clean stops and removes the postgres and keycloak Docker instances, removes the postgres data and DB volumes, and runs rm -rf $KARAF
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/development-workflow.md.hbs:39

## FR-077 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/i18n.md.hbs:578
- target: agent-docs/frontend/i18n.md | src: judo-ng-read | status: validated
- claim: public/i18n/application_hu-HU.json and application_de-DE.json are 'Safe to edit for localization'.
- fact: The same document says application_*.json are generated from the model and regenerated (lines 13-15, 24, 572-573), so application_hu-HU.json
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/i18n.md.hbs:578

## FR-078 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/i18n.md.hbs:256
- target: agent-docs/frontend/i18n.md | src: judo-ng-read | status: validated
- claim: Nested translation keys are accessed as t('entities.fields.title'), t('entities.status.active') and t('validation.required').
- fact: The same document says JUDO uses flat dot-notation keys and not nested objects (line 32); keys such as 'entities.fields.title' or 'validatio
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/i18n.md.hbs:256

## FR-079 [wrong-fact] ### Load Translations from Backend (Advanced)
- target: agent-docs/frontend/i18n.md | src: agent-docs-review:frontend.json | status: reported
- claim: import { L10N_TRANSLATION_PROVIDER_INTERFACE_KEY, L10NTranslationProvider, L10NTranslations } from '~/generated'
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/l10n/l10n-context.tsx.hbs:35,40,42 (exports defined in l10n/l10n-context.tsx)

## FR-080 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/model-screen-layout.md.hbs:242
- target: agent-docs/frontend/model-screen-layout.md | src: judo-ng-read | status: validated
- claim: Generated text field uses t('Entity.View.field', { defaultValue: 'Field' }).
- fact: The key convention documented in i18n.md.hbs is entities.[Entity].[Component].[field] (e.g. entities.User.User_View_Edit.firstName); the 'En
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/model-screen-layout.md.hbs:242


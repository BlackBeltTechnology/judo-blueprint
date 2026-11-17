# advanced-patterns.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/advanced-patterns.md.

## Table of Contents
- Navigation list only; section headings below mirror the source order.

## Dimension Parameters Component System
- Generic component for dynamic parameter groups: multi-line tables, type-aware inputs, add/delete rows, edit vs read-only.
- Props `DimensionParametersComponentProps<T, R>`: `dimensionGroups`, `onValueChange(identifier, propertyName, value)`, `onRowAdd(groupIdentifier, templateParameters)`, `onRowDelete(groupIdentifier, rowIdentifier)`, optional `editMode`, `readOnly`.
- Sections: component interface, type-aware rendering, multi-line table support, integration example.

## Error Interceptor Pattern
- Scaffold `src/custom/hooks/register-error-handler-interceptor.ts.default` exports `registerErrorHandlerInterceptorHook(context)`; copy without `.default`, call from `application-customizer.tsx`.
- Key `ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY` = `'ErrorHandlerInterceptor'`; types from `~/utilities/error-handling`. No `@judo/web-react` package.
- Hook (React hook; may use `useTranslation`, `useSnacks`, `useFaultDialog`) returns `{ shouldInterceptError, interceptError }`. `shouldInterceptError(error, options)` decides; `interceptError(error, options, payload, dataPath)` handles. Runs before default handling.
- Default handling matrix: see Frontend Error Handling. 422 fault body is keyed by the modeled fault object, not `validationResults`.
- Backend shapes: validation errors = list of `{ code, message, location }` (HTTP 400); modeled faults = object keyed by fault (HTTP 422).
- Backend producer code in the source is one project's helper, not a platform API. Use modeled faults and validation in new code.
- Anti-pattern: catching every 5xx and showing a subsystem dialog masks unrelated errors.
- Rule: a subsystem dialog triggers ONLY on an explicit backend `code`. HTTP status alone is not enough.
- Generic 5xx: use an `isGenericServerError` predicate and its own `app.error.server.title` / `.message` i18n pair.

## Pure State Transformation Functions
- Immutable helper functions for nested state updates; return new objects/arrays, no side effects.
- Benefits: immutability, predictability, testability, reusability, generic TypeScript typing.
- Sections: helper functions, usage in components.

## IMaskInput Integration
- Model attribute `textMask` is NOT read by the React generator; no generated widget applies it. Generated app only has `react-imask` as dependency.
- To mask: register a custom implementation element for the field and use `IMaskInput`.
- Examples: phone, currency, date with custom format, custom pattern input; register masked inputs as custom components via hook.

## Cascade Loading Pattern
- Triggers dependent loads on blur (e.g. Country → State → City).
- Real mechanism: no `BlurActionHook` or `BLUR_ACTION_HOOK_INTERFACE_KEY`. Container action type has optional `on<Attribute>BlurAction(...)` for each attribute marked for blur handling (see `types.ts` of generated container).
- Return the handler from the container/page hook created from the `register<Container>ActionsHook` scaffold (see Action Hooks). `createCascadeLoadingHook` returns that handler; `context.actions.*` in examples is illustrative.
- Sections: blur action hook, registration, auto-loading related data, server-side validation on blur.

## PostRefresh Action Hook
- Runs after refresh; syncs UI with server validation or computed fields.
- Real mechanism: no `POST_REFRESH_ACTION_HOOK_INTERFACE_KEY` or `PostRefreshActionHook`. Page and dialog hook types (`<Container>PageActionsExtended`) have optional `post<RefreshAction>` handler (e.g. `postRefreshAction`).
- Return it from the page actions hook from the `register<Page>ActionsHook` scaffold.
- Sections: hook registration, server validation results, calculated fields, status sync, refresh dependent tables.

## Inline Dialog Creation Pattern
- Create and associate nested objects in a modal without leaving the page (e.g. new address while editing a user; new product while creating an order; lookup values; multi-step dialogs).
- Sections: dialog hook, usage example, multi-step inline creation.

## Table Row Highlighting System
- Real API in `~/theme/table-row-highlighting` (`src/theme/table-row-highlighting.ts`).
- `TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY`; `type TableRowHighlightingHook<T> = () => () => RowStylerConfigured<T>[]`.
- Each entry: `{ name, label, condition(params: GridRowClassNameParams<T>), backgroundColor?, fontColor? }`.
- Register with service property `component` = table component name.
- Styling limited to background and font colour (derived per light/dark mode). No `shouldHighlight`/`getHighlightStyle`, arbitrary CSS, borders or row index.
- Stylers evaluated per row; make conditions specific so one applies.
- Sections: hook interface, registration, priority-based, threshold-based.

## Custom Component Replacement
- No generic `CUSTOM_COMPONENT_HOOK_INTERFACE_KEY` or `CustomComponentHook`.
- A custom implementation is a model visual element exposed as extension point: register an `FC` under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` (from `~/custom`) with service property `component` = per-element key from the container's `customization.ts`.
- Scaffold `src/custom/hooks/custom-implementations/register<Container>CustomImplementations.tsx.default` has one `register<Interface>CustomImplementation(context)` per element, with proxy props type (`GenericProxyProps`, `TableProxyProps`, `LinkProxyProps` from `~/custom`).
- Element is created in the ESM UI model as a custom implementation widget; arbitrary generated components are not replaced.
- Date, time and timestamp attributes are `Date` objects in generated types and services (REST strings converted with `new Date(...)`). Compare as `Date` (e.g. by calendar day), not ISO strings.
- Register from `application-customizer.tsx`. `actions.*` props in examples are illustrative; real props = proxy props type in scaffold.
- Sections: component replacement hook, custom dashboard example, custom Gantt chart example, integration with JUDO actions.
- Generated relation service methods (`<Class>ServiceImpl`, from `~/services/data-api/rest`); each present only if the relation allows it; `owner` must carry `__signedIdentifier`; `selected` items serialized as references:
  - `getRangeFor<Rel>` (has range): `(owner?, queryCustomizer?, headers?)` → range list; backs range dialog and autocomplete.
  - `set<Rel>` (settable): `(owner, selected: Target | Array<Target>)`; replaces relation.
  - `unset<Rel>` (optional single relation): `(owner)`; the "clear" for single relation.
  - `add<Rel>` / `remove<Rel>` (collection): `(owner, selected: Array<Target>)`.
  - No `clear` for collections; `set<Rel>(owner, [])` only if settable (verify).
  - Failures throw `AxiosError`; `data` is `FeedbackItem` list (400, 401, 403).

## Configuration Patterns
- Centralised config for timing, defaults, feature flags, API endpoints, retry, page sizes.
- Sections: configuration file, using config in hooks, environment-specific config, configuration hook (`use-config.ts` with context), dynamic updates.

## Best Practices
- General: immutable updates; TypeScript generics; error boundaries; React.memo/useMemo/useCallback where costly; unit-test pure functions; inline docs.
- Hook registration: precise component filters; handle promise rejections; cleanup subscriptions and timers; declare useEffect deps.
- Components: composition over inheritance; single responsibility; context/state for deep props; React.lazy for big components.
- State: colocate; derive rather than store; normalise nested data; optimistic updates with rollback on error.

## Action and Logic Hooks
- Page and container action hooks override action business logic (button clicks, lifecycle). Registered via generated scaffold (container key or `<PAGE>_ACTIONS_HOOK_INTERFACE_KEY`); e.g. `postRefreshAction`.
- Dynamic enumeration filtering: container action hook provides `filter<FieldName>Options(data, options)` returning filtered options.

## Advanced Theming and Rendering
- Sub-themes: `SubThemeHook` registered with unique name; returns theme fragment with MUI `styleOverrides`. Widgets with `subTheme` in model are wrapped in `SubThemeWrapper subTheme="..."` which looks up by `name`.
- Table column customization: `ColumnCustomizerHook` targeted by `component` (table) and `column`; returns new column definition, usually overriding `renderCell`.

## Layout and Navigation Customization
- Table sidekick: custom component above a table; receives `SidekickComponentProps` incl. `onFiltersChange` to filter the table below.
- Dynamic menu: `MenuItemsCustomizerHook` receives generated `menuItems`, returns modified array (add, remove, reorder).
- Multi-tenancy: axios request interceptor injects `X-Judo-RequestParameters` header (e.g. `tenantId` from URL) used by backend for model-driven filtering.
- `NavigationInterceptor` preserves URL query params (e.g. `tenantId`) across navigation.
- Links to Architecture doc for backend filtering.

## Custom Attachments: Token Flow
- Generated `fileHandling` helpers (`downloadFile`, `uploadFile`, `exportFile`, `extractFileNameFromToken`) wrap the two-phase token flow: request `~upload-token`, post multipart with `X-Token`; download with `?disposition=inline|attachment`.
- Details: backend platform behavior reference (client side of upload token flow).

## Related Documentation
- Hooks overview, data hooks, table hooks, action hooks, validation hooks, theming, i18n.

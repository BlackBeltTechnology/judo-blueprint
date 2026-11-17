# model-screen-layout.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/model-screen-layout.md.

## Overview
- Pipeline: ESM model (`.model`) → UI model JSON (`*-ui.json`) → React components (pages, containers, components).
- UI model JSON at `application/frontend-react/model/{project}-ui.json`.

## UI Model JSON Structure
- Top-level keys: `eClass` (`…/ui#//Application`), `@id`, `name`, `navigationController`, `pages`, `containers`, `dataElements`, `enumerationTypes`.
- `name` → module name prefix; `pages` → `src/pages/`; `containers` → `src/containers/`; `dataElements` → TS interfaces + service methods; `enumerationTypes` → TS enums.

## Element ID Format
- `{Actor}/(esm/_{UniqueModelId})/{ElementType}`; e.g. `Actor/(esm/_vbQOQIF3Ee-M3fhNedgt-g)/RelationFeatureView`.
- Discriminated ids for repeated contexts: `…/TableColumn/(discriminator/<tableId>)`.

## ID to data-testid Mapping
- `data-testid` = UI model `@id` exactly. Use with `page.getByTestId()`.
- Layout sections (Flex, accordions, cards, grid wrappers): `data-testid="<xmiId>"` + `data-name="<element name>"`. Select via `[data-name="<Name>"]`; name must be unique per page. Page header: `data-name="PageHeaderContainer"`.
- Container layout not swappable by hook. Replace via custom implementation element on the container's visual element, or override `containers/widget-fragments/flex.hbs` (same-name template override in generator override dir).

## Page Container Types
- No per-device containers. Section width = `col` of 12 (scaled by parent `col`), applied from `md` up; below `md` full width (`xs: 12, sm: 12`). Device-specific: custom implementation with MUI `useMediaQuery`.
- `EmptyDashboardPageContainer`: landing page with no widgets. Page `dashboard: true`. Generated `src/pages/Dashboard/index.tsx`, `src/containers/Dashboard/EmptyDashboard*.tsx`.
- `TransferObjectFormPageContainer`: CREATE forms. `openInDialog`, `dialogSize` (`XS|SM|MD|LG|XL`). Generated `src/containers/{Entity}/{Entity}_Form/`.
- `TransferObjectTablePageContainer`: LIST in DataGrid. Generated `src/containers/{Entity}/{Entity}_Table/` + `components/{Entity}_TableComponent/`. IDs: `…TableContainer`, `…TableTable`.
- `TransferObjectViewPageContainer`: VIEW/UPDATE. Generated `src/containers/{Entity}/{Entity}_View_Edit/`. IDs: `…ViewPageContainer`, `…ViewVisualElement`.

## Visual Element Types (Field Inputs)
- String → `StringTypeTextInput` (TextField); multiline → `StringTypeTextArea`; read-only → `StringTypeFormatted` (span).
- Boolean → `BooleanTypeCheckbox`. Numeric/Double → `NumericTypeVisualInput` (NumericInput).
- Date → `DateTypeInput` (DatePicker); Timestamp → `TimestampTypeDateTimeInput` (DateTimePicker); Time → `TimeTypeTypeTimeInput` (TimePicker).
- Binary → `BinaryTypeInput` (FileInput). Email → `StringTypeTextInput` as `type="email"`.
- Enumeration: `EnumerationTypeToggleButtonbar` (ToggleButtonGroup), `EnumerationTypeCombo` (Select), `EnumerationTypeRadio` (RadioGroup).
- Generated TextField: `name`, `data-testid` = `@id`, label key `entities.[Entity].[Component].[field]` with `defaultValue`, `disabled={isLoading}`, `error`/`helperText` from `validation`, `onChange` → `storeDiff`. See `i18n.md`.
- Layout elements: `DividerVisualElement`, `TextFieldVisualElement` (static text), `PlaceholderVisualElement`, `TabBarVisualElement`.

## Relation Element Types
- Single link: `TabularReferenceFieldRelationDefinedLink` — Autocomplete with view/set/unset.
- Multiple table: `TabularReferenceFieldRelationDefinedTable` — DataGrid with toolbar and row actions.
- Relation button: `TabularReferenceFieldButton` — opens relation in page/dialog.

## Action Definition Types
- Page-level (suffix): BackActionDefinition `*BackButton`; CreateActionDefinition `*CreateButton`; UpdateActionDefinition `*UpdateButton`; DeleteActionDefinition `*DeleteButton`; CancelActionDefinition `*CancelButton`; RefreshActionDefinition `*RefreshButton`; GetTemplateActionDefinition `*GetTemplateButton`.
- Table: FilterActionDefinition `*FilterButton` (filter dialog); RefreshActionDefinition `*RefreshButton`; ExportActionDefinition `*ExportButton`; OpenCreateFormActionDefinition `*CreateButton`; OpenAddSelectorActionDefinition `*AddSelectorButton`; OpenSetSelectorActionDefinition `*SetSelectorButton`; ClearActionDefinition `*ClearButton`; BulkRemoveActionDefinition `*BulkRemoveButton`; BulkDeleteActionDefinition `*BulkDeleteButton`; InlineCreateRowActionDefinition `TabularReferenceTableInlineCreateButton`.
- Row: OpenPageActionDefinition `*RowViewButton`; RemoveActionDefinition `*RowRemoveButton` (remove relation); RowDeleteActionDefinition `*RowDeleteButton` (delete entity).
- Custom operations: `OperationFormVisualElement` (operation button), `OperationFormCallButton` (submit), `OperationFormTableRowCallOperationButton` (row-level), `OperationMenuButton` (static/menu), `ActionButtonVisualElement` (standalone Ok/Cancel).

## File Path Generation Patterns
- Pages: factory `#getPagesForRouting(#application)`; `src/pages/{PagePath}/index.tsx` + `context.tsx`. e.g. `TagContainerTransfer::manyAssociationAssociation::RelationViewPage` → `src/pages/TagContainerTransfer/ManyAssociationAssociation/RelationViewPage/index.tsx`.
- Containers: factory `#application.pageContainers`; `src/containers/{ContainerPath}/{Name}.tsx`, `{Name}PageContainer.tsx`, `{Name}DialogContainer.tsx`, `components/{ComponentName}/index.tsx`.
- Component names: `{TransferObjectName}{ViewType}{RelationName}Component`.

## Navigation Controller and Actor Accesses
- Menu driven by Actor's `accesses`; each becomes a sidebar item. ESM: `<elements xsi:type="accesspoint:ActorType" name realm principal>` + `<accesses name target>`.
- `navigationController` items: `label`, `target` ($ref to page definition). Generated `src/layout/Drawer/DrawerContent/Navigation/menu-items.tsx`. Target determines page type.
- Control attributes (static on ESM element or dynamic from backend):
  - `hiddenBy`: hidden completely when true.
  - `enabledBy`: enabled (clickable/editable) when true.
  - `requiredBy`: field required when true.
- Example expressions: `hiddenBy="self.user.role != 'ADMIN'"`, `enabledBy="self.user.isActive"`.
- Interceptor-driven: backend `preRead` sets boolean DTO attributes (e.g. `canManageUsers`) on the TO; ESM `DERIVED` boolean attributes with `getterExpression="false"`; relations `hiddenBy="not self.canManageUsers"`.
- Same attributes apply to relations and attributes (`salary` with hiddenBy/enabledBy/requiredBy). Generated: `!data.hiddenBy &&` render, `disabled={!data.enabledBy}`, `required={data.requiredBy}`.
- Hidden relation: table/link not rendered, nav buttons hidden, tab removed.
- Summary: `hiddenBy=true` → menu item hidden / tab not rendered / field not rendered. `enabledBy=false` → menu visible greyed / table read-only / field disabled. `requiredBy=true` → required validation.

## Data Element Types
- ClassType: `eClass …/ui#//data/ClassType`, `name`.
- RelationType: `target`, `isCollection` (true = 1:N), `isAssociation` (true = association, false = composition), `isDerived` (read-only).

## Page Definition Properties
- `openInDialog`, `dialogSize` (XS–XL), `dashboard`, `generateActionsHook` (generate actions hook for customization), `isSelector`, `isRelationSelector`.

## Action References
- Page `actions[]`: `actionDefinition` ($ref to type definition), `targetPageDefinition` (navigation), `ownerDataElement`, `isMenuAction` (true → dropdown menu).

## Discriminators in IDs
- Same element type in several contexts (e.g. a column in several tables) gets `(discriminator/<parent @id>)` appended, keeping IDs unique.

## Container Hook Registration
- Each container generates a hook key `<CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY` = `'<Container>ContainerHook'`.
- Container consumes it via `useTrackService<…>` with the LDAP-style filter `(${OBJECTCLASS}=<KEY>)`; calls `customContainerHook?.(data, editMode, storeDiff) || {}`.
- Generated page folder `src/pages/<Page>/`:
  - `index.tsx`: loads data, builds page actions (merged with custom hook), renders container inside view-model provider.
  - `context.tsx`: `<Container>ViewModel` (page props + `setIsLoading`, `setEditMode`, `refresh`, `selectionDiff` on selector pages), `<Container>ViewModelContext`, `use<Container>ViewModel()`. Throws outside provider.
  - `customization.ts`: `<PAGE>_ACTIONS_HOOK_INTERFACE_KEY` and type `<Container>ActionsHook = (data, editMode, storeDiff?, selectionDiff?, refresh?, submit?) => <Container>PageActionsExtended`.
  - `types.ts`: `<Container>PageActionsExtended` (container action types plus optional `post<Action>` handlers) and `<Page>XMIID` constant.
- `src/config/layout.ts`: app-wide layout constants (`DRAWER_WIDTH`, `MINI_DRAWER_WIDTH`, `DIVIDER_HEIGHT`, `SUBMENU_MIN_WIDTH`), enums (`ThemeMode`, `MenuOrientation`, `ThemeDirection`), `defaultLayoutConfig` (menu orientation from model; light mode, header on, boxed), `menuBehaviour`. Do not edit; regenerated.

## Service Generation
- Paths: `src/services/data-axios/{Entity}ServiceImpl.ts` and `{Entity}ServiceFor{Relation}Impl.ts`.
- Methods: `refresh(target, queryCustomizer)`, `validateUpdate(target, selected)`, `update(target, selected)`, `delete(selected)`.

## Best Practices
- Find element IDs: UI model JSON (by name/type), `data-testid` in generated code, DevTools.
- Customization points: container actions hook; page actions hook; field disabled/required/readonly hooks; custom components via Pandino DI.
- Testing: `page.getByTestId('<@id>')`, or `VisualElementIds` constant (e.g. `EntityName_Form.fieldName.id` from `../helpers/visualElementIds/VisualElementIds`).

## ESM to UI Model Mapping
- memberType on relations:
  - `MAPPED`: full CRUD by flags. Form: yes; Table: yes with Create; actions: InlineCreate, AddSelector, RowDelete, BulkDelete.
  - `DERIVED` (`getterExpression`): no Create; Update/Delete limited. Form: no; Table: yes without Create; delete actions RowDelete, BulkDelete.
  - `TRANSIENT`: view only; no CRUD actions.
- Relation flags: `createable` → `OpenCreateFormActionDefinition`, `InlineCreateRowActionDefinition`, `OpenAddSelectorActionDefinition`. `updateable` → `UpdateActionDefinition` on view pages. `deleteable` → `RowDeleteActionDefinition`, `BulkDeleteActionDefinition`, `DeleteActionDefinition`.
- `relationKind`: absent = association (link selector, add/remove); `AGGREGATION` = owned collection (add/remove/create); `COMPOSITION` = create/delete, no remove (cascade).
- Cardinality: `lower`/`upper`: 0..1 → single link (Autocomplete); 1..1 → required single link; 0..unbounded → table; 1..unbounded → table with min 1.
- Two-way relations: `partner` attribute; `primary="true"` side gets table view with CRUD.
- Entity flags `createable`/`updateable`/`deleteable` on `EntityType` apply to all TOs mapped to it.
- Operations: `operationType` `MAPPED` → `ui:OperationForm` (view page, table row); `STATIC` → `ui:MenuItemOperation` (actor menu); bound with no type → `ui:OperationForm` (entity view/form).
- Operation input → submit dialog; output → result display.
- `ui:OperationForm` `confirmationMessage`, `confirmationType`: `MANDATORY` (always) | `CONDITIONAL` (by condition) | absent (none).
- `ui:ActionGroup` `featuredActions="N"`: N actions visible before menu.
- `ui:ActionButton` with `action="CANCEL"` for cancel.
- Attribute types → UI: StringType → TextField/TextArea; NumericType → NumericInput; BooleanType → Checkbox/Switch; DateType → DatePicker; TimestampType → DateTimePicker; TimeType → TimePicker; EnumerationType → Select/RadioGroup/ToggleButtons; BinaryType → FileUpload.
- Attribute flags: `required` (validation), `defaultExpression` (initial value), `memberType` (`MAPPED` | `DERIVED`), `getterExpression` (DERIVED computation).
- Actor type: `accesses` → nav menu items, actor-specific routes, role-based access control.
- Traceability: ESM `xmi:id` preserved in UI `@id` and `data-testid`; use to target hooks at specific elements.
- Decision tree: CRUD → ESM `createable`/`updateable`/`deleteable`; relation type → `memberType`; cardinality → `lower`/`upper`; custom op → add ESM operation; UI-only change → frontend hook.

## See Also
- `README.md` (frontend overview), `hooks/README.md`, `../e2e-testing/model-screen-layout.md`, `../model/README.md`.

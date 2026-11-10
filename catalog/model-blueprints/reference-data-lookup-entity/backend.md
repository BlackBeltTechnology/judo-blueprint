## Backend guidance

Plain lookups need no custom backend code. The generated DAO covers read, and the project's access and transfer objects decide who may write. Backend code appears only for seeding, name checks and bulk management.

### Seeding at startup

Initial rows are created once by a static initializer operation with the generated DAO. In the source projects the initializer seeds cities (about 250, with postal code links), capabilities and similar lists. The initializer is project code, not a platform hook. See [[init-data-seeding]].

### Management through a shared service

One project service (in the source project `MasterDataService`, an example name) holds create, update and toggle-active for the lookups. The custom operations are thin wrappers that delegate to it. Its main job is the rule the model does not express: name uniqueness checked before create and update. The service and operation classes are project code, not platform API. Interceptors do not run for custom operations, so the rule lives in the service. See [[capability-lookup-entity]] for the same shape with a flag.

### Resolving selected entries

An operation that receives a multi-select resolves the chosen entries by identifier through the generated DAO. The DAO's `getById` fetches one entry. In the source project the selected names are then joined into one denormalized string for display, which is project practice, see [[aggregated-stored-field]]. Many-to-many links are changed with the generated per-relation `add` and `remove` methods. Remember the generated DAO rules: `add` and `remove` fail on a null element, and an optional single relation is cleared with `unset`, not `set(null)`. See [data access guide](../../agent-docs/backend/data-access-guide.md).

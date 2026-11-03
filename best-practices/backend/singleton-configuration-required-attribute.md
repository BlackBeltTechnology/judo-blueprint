---
id: "singleton-configuration-required-attribute"
title: "Adding a Required Attribute to a Singleton Configuration Entity (Full Edit-Surface Ripple)"
domain: "backend"
category: "model-and-config"
score: 70.0
usage_count: 1
alternative_count: 1
first_seen: "2026-07-13"
last_updated: "2026-07-13"
projects:
  - park-here
---
## Description

Adding a new **required** attribute (scalar, enum, or `Binary`/`FileType`) to a singleton "settings" entity such as `Configuration` is never a one-line model change. The `required` flag ripples across the entity's entire read/write/edit surface, and missing any one site fails the build, a test, or the settings screen at runtime. Plan the full ripple before touching the model.

The email template attributes on park-here's `Configuration` are the canonical example: `deletationEmailTemplate`, `reminderEmailTemplate`, `travelReminderEmailTemplate`, etc. each appear in **five** places, not one.

## The ripple surface (mirror an existing sibling attribute end-to-end)

For a new required attribute `fooTemplate` on `Configuration`, mirror an existing sibling (e.g. `deletationEmailTemplate`) at **every** site:

1. **Entity attribute** — `ParkHere::entities::Configuration.fooTemplate` (`STORED`, `required=true`). Generates `getFooTemplate()` / `withFooTemplate()` on the default entity TO + `ForCreate` builder.
2. **Input TO** — `ParkHere::services::ConfigurationInput.fooTemplate` (`TRANSIENT`, `required=true`). This is the operation write-DTO. **A required member here means the settings form MUST supply it or the operation call fails validation.**
3. **Display/settings TO** — `ParkHere::services::ConfigurationSettings.fooTemplate` (`DERIVED`, getter `ParkHere::entities::Configuration!any().fooTemplate`). Auto-populates the settings screen from the current entity.
4. **UI `DataField`s** — one per form/view that edits settings (park-here has four: `ConfigurationInput_Form`, `ConfigurationInput_View_Edit`, `ConfigurationSettings_Form`, `ConfigurationSettings_View_Edit`), each bound via `dataFeature` to the matching member. Without these, the required input member is never populated → settings save breaks.
5. **`ConfigurationServiceImpl.saveConfiguration`** — set the new field on **both** the create branch (`ConfigurationForCreate.builder().withFooTemplate(...)`) and the update branch (`configuration.get().setFooTemplate(...)`). Missing the create branch fails create-time validation.
6. **Initial-data loader** (`InitCustomImplementation`) — seed the value for fresh/empty projects (for templates: `fileStoreService.put(...)` + reference from the seeded `Configuration`).
7. **Every test/fixture that builds a `Configuration`** — a new required attribute breaks all of them until updated. In park-here that was `TravelTestFixtures.createConfiguration`, `ConfigurationUpsertBufferTest`, `QuickReservationMorningBufferTest`, `ReportRecipientsTest`. Grep the whole tree for `ConfigurationForCreate` / `setDeletationEmailTemplate` / `withDeletationEmailTemplate` to find them all.
8. **Existing persisted rows** (local/staging/prod DBs) — the RDBMS column is added *nullable* (JUDO enforces `required` at the app layer, not via a DB `NOT NULL`), so existing rows get `NULL` and break app-layer validation / NPE the reader. A data **backfill** is required (see the schema-evolution guide, "New required Binary/FileType attribute backfill").

## Alternative (rejected): make the attribute optional

Making the attribute `required=false` avoids the create/update/UI ripple entirely (the reader just null-guards, mirroring the existing `travelReminderEmailTemplate` null-guard in `sendReminders`). Choose this when the attribute is genuinely optional and does **not** need to be consistent with the other required settings or editable from the settings screen. It is the smaller, non-breaking change — but it is not "mirror the existing templates".

## FileStoreService has no lookup-by-name — you MUST persist the id

`hu.blackbelt.osgi.filestore.api.FileStoreService` exposes only `put(stream, fileName, mime) -> String id`, `get(id)`, `exists(id)`, etc. There is **no** "get by name". `put` returns a *generated* id; the second arg is a display filename, not a handle. Therefore the only way a service can recover an uploaded template/file at runtime is to read its generated id back from a **persisted `Configuration` attribute** (`configuration.getFooTemplate().getId()`). This is exactly why every uploadable template on `Configuration` needs its own model attribute — you cannot look one up by a well-known name.

## Verification

- `openspec validate <change> --strict` passes.
- `./judo.sh build -F` (backend) compiles — the SDK regenerates `getFooTemplate`/`withFooTemplate`.
- Every `Configuration`-creating test passes (grep for the ripple sites first).
- Existing DB rows are backfilled (0 NULLs in the new column) — see schema-evolution guide.

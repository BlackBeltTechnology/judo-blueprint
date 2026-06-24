## Overview

The generated React frontend renders the transient single-select relation as an `AggregationInput` widget. The widget shows the currently selected target instance (or an empty state with a Create / Set icon), opens a `RangeDialog` in single-select mode to pick a different instance, and writes the selection back into the form's input state. Data for the dialog is fetched via the generator-emitted `getRangeFor<rel>()` service method on the operation's service implementation.

For the underlying widget itself see [`aggregation-input-widget`](../../best-practices/frontend/aggregation-input-widget.md); for the action-group / page-routing wrapping see [`action-group-input-output-routing`](../../best-practices/frontend/action-group-input-output-routing.md).

## Widget Recipe

```typescript
<AggregationInput
  label="Region"
  labelList={[data.region?.name ?? '']}
  value={data.region}
  readonly={!editMode}
  onSet={async () => {
    const res = await openRangeDialog({
      columns,
      rangeCall: (queryCustomizer) =>
        viewCreateInitiativeServiceImpl.getRangeForRegion(data, queryCustomizer),
      single: true,
    });
    if (res) setData({ ...data, region: res });
  }}
  onRemove={() => setData({ ...data, region: null })}
/>
```

Key bindings:
- **Service call**: `getRangeFor<rel>(template, queryCustomizer)` — generator emits one per transient relation with `RANGE` behavior. The first argument carries the current input template (so range expressions can reference other fields on the input); the second carries pagination / filter customizer state.
- **Dialog mode**: `single: true` — the dialog returns a single row (or null on cancel).
- **State write-back**: assign the chosen row into `data.<rel>`; on submit, `data` is sent as the operation argument and the body's `mutable input.<rel>` converts it to a stored reference.

## Runtime Sequence

```mermaid
sequenceDiagram
  autonumber
  participant U as User
  participant V as React view<br/>(operation input page)
  participant S as Generated service<br/>(*ServiceImpl)
  participant D as Dispatcher
  participant DAO as DAO / DB

  Note over V: page loaded with empty *Input template<br/>(transient relation = null)

  U->>V: click AggregationInput → Set
  V->>S: getRangeFor<rel>(template, queryCustomizer)
  S->>D: range dispatch (filtered by range expr)
  D->>DAO: SELECT * FROM <mapped_entity><br/>WHERE <range filter>
  DAO-->>D: page
  D-->>S: page<TargetTO>
  S-->>V: rows
  V-->>U: RangeDialog opens (single: true)

  U->>V: select row → setData
  Note over V: input.<rel> now holds<br/>a JudoIdentifiable reference<br/>(NOT persisted yet)

  U->>V: submit operation
  V->>S: operation(input)
  S->>D: op call
  D->>D: body executes:<br/>mutable input.<rel> ⇒ stored ref
  D->>DAO: INSERT/UPDATE owning entity<br/>with FK to selected target
  DAO-->>D: ok
  D-->>S: result
  S-->>V: navigate / refresh
```

## Examples

### itracker
- **Widget**: `InititativeInput.region` rendered as a single `AggregationInput` on the `createInitiative` input page.
- **Service**: `getRangeForRegion(template, queryCustomizer)` returns the paginated list of `Region` instances (filtered by the optional range expression).
- **UX**: user clicks the field's Set icon, picks a region, the dialog closes, and `data.region` is populated. On submit, the new `Initiative` is created with the selected region linked via `mutable input.region`.

## Frontend guidance

The component is project code. Names below are illustrative; the real props type and registration key come from the generated code of the form.

### Register a custom visual element

Replace the generated group for the sensitive field with a custom visual element. The platform exposes the group as an extension point: register a function component under the custom visual element key, with the group's generated component key as service property. Call the register function from the application customizer. See [advanced patterns](../../agent-docs/frontend/advanced-patterns.md) and [[custom-visual-element-override]].

### Toggle the input type

Keep the type in component state: `text` while editing, `password` after blur when the field has a value, and back to `text` when the value is cleared.

```tsx
const [type, setType] = useState<'text' | 'password'>('text');
<NumericInput
  type={type}
  value={data.rate}
  onFocus={() => setType('text')}
  onBlur={() => setType(data.rate != null ? 'password' : 'text')}
  onValueChange={(v) => {
    storeDiff('rate', v);
    if (v == null) storeDiff('rateRepeat', undefined); // clear the repeat field too
  }}
/>
```

### Enable the repeat field late

Disable the repeat field while loading or while the primary value is empty. Show field errors from the validation object for both fields.

### Patch the read-only flag

The generated form computes read-only state. A replacement component does not get that for free, so set read-only to false (or compute it from the edit mode) on both inputs. In the source project both fields are patched this way.

### Validation

A form action hook on the same dialog may return extra validation props, for example disabling future dates for a date field. Checking that the two values match is done by a validator or on the server. The UI check does not replace the server check. See [validation hooks](../../agent-docs/frontend/hooks/validation-hooks.md) and [action hooks](../../agent-docs/frontend/hooks/action-hooks.md).

### Source project

React. One custom element replaces the rate group on a create form (decimal scale of four places). A separate form action hook on the same dialog blocks future dates. Masking also stops copy and paste between the two fields.

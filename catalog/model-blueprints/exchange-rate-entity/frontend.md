## Frontend guidance

### Block future dates on the input form

Set the date picker so that future dates cannot be chosen when the rate is entered. The check belongs in the form's action hook, which returns the picker's validation props (disable future dates). The backend validation still applies, so the UI check is a convenience, not the rule.

### Mask a sensitive rate and require a second entry

Treat the entered rate as sensitive: after the user enters the rate and leaves the field, mask the value. Enable the repeat field only after a rate is entered, so the user types the rate twice. See [[sensitive-field-double-entry-verification]] for the full pattern.

### Replace the generated group with a custom element

The generated form shows the rate and its repeat as two separate inputs. A custom form element replaces that group with one component that holds both inputs, so the masking and the enable rule stay together.

## Examples

### rackinspect

- The custom rate group replaces the generated rate input on the create-rate form. The rate field switches to a masked input after blur, and the repeat field is disabled until a rate is entered.
- The form action hook disables future dates on the date picker.
- The masking is specific to this project: it treats exchange rates as semi-confidential data that needs double-entry confirmation.

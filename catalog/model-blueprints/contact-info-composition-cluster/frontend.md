## Frontend guidance

### Edit contacts as lists on the parent

The parent's form shows each contact kind as an editable list, with its own add and remove actions. The generated forms for the contact entities are not used directly.

- Show the active flag as a switch on each row. Use the toggle-active operation for it so the backend rules run.
- Choose the primary from the e-mail list with a radio button. Setting it calls the toggle-primary operation.
- Mark inactive rows visually, but keep them in the list so the history stays readable.

### Format address text from its parts

An address field can compute its full text from the street, city and postal code on blur. Compute it in the form only when the user has not typed the full text by hand.

## Examples

### Variant seen in practice

- Framework: React.
- Address hooks compute the full address from its parts on blur, in both the form and the view-edit page.
- E-mail, phone and bank-account lists use the generated frontend without custom hooks; the toggle operations appear as standard actions.

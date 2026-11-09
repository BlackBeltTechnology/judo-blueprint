## Frontend guidance

### Replace the generated sign-in with a two-step dialog

The generated pages do not fit this flow. Build a two-step dialog: first collect the e-mail and name and call register; then show a code input and call activate. The generated Form for User stays hidden.

- The code input is a row of single-digit fields that move focus forward on each entry.
- Submit the activation automatically when the last digit is entered. A button is not needed.
- After activation, store the e-mail and an identifier locally so the session survives a page reload. Clear it on reset.

### Handle an invalid code by re-opening the registration

When the activate call returns the generic invalid-code fault, show the registration dialog again. The stored session is no longer valid.

### Custom styling is optional

Shared dialog, card and button components can give the flow a consistent look. This is a presentation choice, not part of the pattern.

## Examples

### trivia

- Framework: React.
- The player frontend replaces the generated navigation with a custom single-page layout, because the flow must run before any generated page is available.
- The code input auto-submits on the fourth digit.

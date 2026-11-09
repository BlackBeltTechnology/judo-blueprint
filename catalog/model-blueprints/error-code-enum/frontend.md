## Frontend guidance

### Show the business error message from a 422 response

A business error arrives as HTTP 422. The response body is keyed by the fault's type name, and the business error's `message` is the text to show. An error hook for the 422 status reads that message and shows it as a snack, rather than the generic fault dialog. See [[error-handler-interceptor-customization]].

### Translate the codes, not the messages

When the application has an enumeration of codes, provide a translation for each member. The client shows the translated text for the code, and falls back to the message. The message is for people; the code is for branching.

### Branch on the code only when the flow needs it

In a custom screen, the code can drive the flow (for example, send the user to registration on an invalid code). Convert the numeric code to the enumeration member and branch on it. Do not branch on the message text.

### Do not show a field error as a business error

A field error from the field validation mechanism belongs under its field. A business error is shown as a single message. Keep the two paths separate in the hook.

## Examples

### mlszksz-platform

- The project uses plain string codes, so the hook shows the message text only and needs no enumeration translation.
- The hook checks for status 422, reads the message from the first key of the response body, and shows it for three seconds.

### indamedia-adtrack and park-here

- The projects with an enumeration provide a translation for each member, and the hook shows the translated text.

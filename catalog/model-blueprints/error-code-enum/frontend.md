## Frontend guidance

### Show the business error message from a 422 response

A business error arrives as HTTP 422 with an `X-Fault` header. The response body is an object with two keys: the fault's type name (holding the business error's `message`) and a `code` key. The business error's `message` is the text to show. By default the generated handler takes only the first key of the body; the server sorts the keys, so that is usually `code` rather than the fault name, and the handler opens the fault dialog for it, which shows every detail as a key and value; labels come from translation keys `faults.<fault name>.<attribute>` and fall back to the raw attribute name. Common practice: an error hook for the 422 status reads the message instead and shows it as a snack. See [[error-handler-interceptor-customization]].

### Translate the codes, not the messages

When the application has an enumeration of codes, provide a translation for each member. The client shows the translated text for the code, and falls back to the message. The message is for people; the code is for branching.

### Branch on the code only when the flow needs it

In a custom screen, the code can drive the flow (for example, send the user to registration on an invalid code). Convert the numeric code to the enumeration member and branch on it. Do not branch on the message text.

### Do not show a field error as a business error

A field error from the field validation mechanism belongs under its field. A business error is shown as a single message. Keep the two paths separate in the hook.

## Examples

### Variant seen in practice

- One project uses plain string codes, so the hook shows the message text only and needs no enumeration translation.
- The hook checks for status 422, reads the message from the first key of the response body, and shows it for three seconds.

### Second variant seen in practice

- The projects with an enumeration provide a translation for each member, and the hook shows the translated text.

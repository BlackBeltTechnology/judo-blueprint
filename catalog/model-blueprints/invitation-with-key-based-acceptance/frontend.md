## Frontend guidance

### Let the anonymous page read the key from the link

The acceptance page belongs to an anonymous actor, so it is reached without signing in. The platform's guest-page hook (`supportGuestAccess`) only governs what an unauthenticated visitor sees at the root; this entry's page is an anonymous actor's own app. It reads the key from the query parameter of the link, and sends the key with each API call so the backend can find the invitation. Register one request interceptor for this (the generated frontend uses an axios request interceptor for header enrichment, see the platform's advanced patterns), not one per call. The key-in-URL scheme is common practice.

### Redirect after accept or cancel

After a successful accept or cancel, leave the anonymous page and send the user to the signed-in area. Do this in a post-operation action hook for the page. Use the hook key the framework generates for that page and container.

### Keep the key across navigation

If the anonymous page navigates between its own screens, carry the key through the navigation with a navigation interceptor (`decorateNavigation`), which can rewrite the target path but cannot cancel navigation. Otherwise the second screen loses the key and the accept call fails.

### Mask the password fields

The accept form holds the password and its confirmation. Render both as password inputs. The generated form is the default; override it only for this masking, and keep the override in the custom folder so a regeneration does not overwrite it.

### Show the expired state

When the backend refuses an expired or unknown key, show a clear message and no form. Do not show the accept form for an invitation the backend has already refused.

## Examples

### Variant seen in practice

- The anonymous actor's app registers the key-forwarding interceptor and a navigation interceptor so the key is kept.
- Two post-operation hooks redirect to the signed-in account app after accept and after cancel.
- The accept parameter form masks the password and its confirmation.

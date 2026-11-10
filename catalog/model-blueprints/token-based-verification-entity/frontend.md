## Overview

The token-based verification flow runs in a separate frontend application. It has three custom pages: organization registration, email verification and invitation verification. These pages are written by hand, not generated, because the flow runs before any user is signed in.

## Implementation pattern

- **Separate application.** The registration flow has its own application and its own actor, so it does not depend on the main authenticated app.
- **Registration page.** A multi-section form collects the organization details and the company administrator. It reads a token and an email from the URL when the registration comes from an invitation. It runs a bot check before it submits.
- **Verification pages.** Each page reads an identifier and a token from the URL, then calls the matching verification operation. The page shows a status-driven state (idle, loading, success, error, invalid).
- **Bot check.** A shared hook provides a token for the bot check, and each verification action requests one first.
- **Hook keys are generated per page or container.** Custom hooks on the generated pages must use the key that the generator produces for that page ([Advanced frontend patterns](../../agent-docs/frontend/advanced-patterns.md#page-and-container-action-hooks)). The three custom pages here are not generated, so they do not use generated hook keys.
- **Localization.** The registration app keeps its own translation file for the registration and verification text.

## Examples

### mlszksz-platform

- Framework: React (example project code).
- Key files: the registration page, the verification page, the invitation verification page and the bot-check hook in the registration app.
- Each page calls its backend operation through the registration app's generated service client. The registration form uses controlled inputs with client-side validation.
- The registration app ignores generated output for its custom pages and its HTML entry, so regeneration does not overwrite them.

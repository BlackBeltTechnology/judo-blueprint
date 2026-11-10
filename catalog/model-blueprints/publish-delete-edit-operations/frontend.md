## Overview

The generated UI already shows publish, delete and edit buttons for the content transfer object. The buttons are hidden or shown from the guard flags. Custom frontend code is needed only to pre-fill the edit form, because the edit operation takes its own input type rather than the content's mapped type.

## Implementation pattern

- Keep the generated publish and delete buttons. Their visibility follows the guard flags (for example "is not publishable"). The flags only hide or disable controls; the backend operation still checks the status.
- For the edit form, add a form-actions hook on the edit dialog. The hook fetches the current content and writes each field into the form. Hook code lives in the gitignored `src/custom/` folder, so it survives regeneration.
- Hook registration keys are generated per page and per container. Use the key the generator produces for your page; do not copy a key from another page or project.
- Pre-fill only fields the edit operation accepts. Fields that are not in the input type are read-only and are not sent.

## Examples

### mlszksz-platform

- Framework: React with a registration-based hook system (project code).
- The company-admin edit dialogs for news, offer, request and the admin announcement dialog each have a form-actions hook. Each hook reads the content with the parent service and a content-specific mask, then writes each field into the form.
- The publish, delete and moderation buttons use the generated UI with no custom rendering.

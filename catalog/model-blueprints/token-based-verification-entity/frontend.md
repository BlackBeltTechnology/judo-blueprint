## Overview

The token-based verification entity manifests in the React frontend through a dedicated registration application with three custom pages: organization registration, email verification, and invitation verification. These pages are fully custom (not generated) and handle the token-based verification workflow.

## Implementation Pattern

- **Separate frontend application**: The registration flow runs in its own React app (`mlszkszplatform__services__registration__registration_point`) with a separate actor (RegistrationPoint), completely independent from the main authenticated app.
- **RegistrationPage**: A multi-section form collecting organization details, address, contact info, and company admin credentials. Supports both direct registration and invitation-based registration (reads `token` and `email` from URL query params). Uses reCAPTCHA validation before submission.
- **VerificationPage**: Reads `id` and `token` from URL search params, displays a status-driven UI (idle/loading/success/error/invalid), and calls the `validate` operation on the RegistrationTransfer TO to verify the registration token.
- **InvitationVerifyPage**: Similar to VerificationPage but for user invitation tokens. Reads `id` and `token` from URL search params and calls `verifyUserInvitation` on the RegistrationTransfer TO.
- **reCAPTCHA integration**: A custom `useRecaptcha` hook provides `getRecaptchaToken()` for bot protection on all verification actions.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `registration_point/src/custom/pages/RegistrationPage.tsx`, `registration_point/src/custom/pages/VerificationPage.tsx`, `registration_point/src/custom/pages/InvitationVerifyPage.tsx`, `registration_point/src/custom/hooks/useRecaptcha.ts`
- Pattern: Each page is a standalone React component using `RegistrationPointServiceForRegistrationTransferImpl` to call backend operations. The registration form uses controlled inputs with client-side validation (FormErrors). Verification pages use a state machine pattern (idle -> loading -> success/error) to manage the asynchronous verification flow.
- Notable: The registration app has its own `.generator-ignore` entries for custom pages and `index.html` (with reCAPTCHA script). i18n translations for registration/verification are in a separate `application_hu-HU.json` file in the registration app.

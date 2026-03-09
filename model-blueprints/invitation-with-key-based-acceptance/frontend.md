## Overview

The invitation-with-key-based-acceptance blueprint has extensive React frontend customization across the anonymous actor application. The anonymous actor handles the unauthenticated invitation acceptance flow: a custom axios interceptor extracts the `invitationKey` query parameter from the URL and passes it as a request header, custom Pandino action hooks redirect the user to the authenticated actor after accepting or canceling an invitation, and the AcceptInvitationLinkParamater form is overridden via generator-ignore to mask password fields.

## Implementation Pattern

- **Axios interceptor for invitation key**: The anonymous actor's `application-customizer.tsx` registers an axios request interceptor that extracts the `invitationKey` query parameter from `window.location` and injects it as `X-Judo-RequestParameters` header on every API call. This allows the backend to identify which invitation is being accessed from the URL alone.
- **Navigation interceptor**: A `NavigationInterceptorHook` is registered to preserve search parameters (including the invitationKey) across internal navigation, so the key is not lost during page transitions.
- **Post-action redirect hooks**: Two custom Pandino action hooks handle post-operation flow:
  - `registerServicesAnonymousActorInvitationAccessViewPageActionsHook` -- overrides `postCancelInvitationForInviteLinkAction` to redirect to the AccountActor app after cancellation.
  - `registerServicesInviteLinkInviteLink_View_EditAcceptInvitationInputFormActionsHook` -- overrides `postAcceptInvitationForInviteLinkAction` to redirect to the AccountActor app after successful acceptance.
- **Password field masking**: The generated `AcceptInvitationLinkParamater_Form` container is listed in `.generator-ignore` and overridden to add `type="password"` to the password and passwordAgain TextField components, ensuring credentials are masked during input.

## Examples

### ubives
- Framework: React
- Key files: `ubives__services__anonymous_actor/src/custom/application-customizer.tsx`, `ubives__services__anonymous_actor/src/custom/hooks/pages/registerServicesAnonymousActorInvitationAccessViewPageActionsHook.ts`, `ubives__services__anonymous_actor/src/custom/hooks/dialogs/registerServicesInviteLinkInviteLink_View_EditAcceptInvitationInputFormActionsHook.ts`, `ubives__services__anonymous_actor/src/containers/Entities/AcceptInvitationLinkParamater/AcceptInvitationLinkParamater_Form/EntitiesAcceptInvitationLinkParamaterAcceptInvitationLinkParamater_Form.tsx`
- Pattern: The anonymous actor's application-customizer registers an axios interceptor to extract `invitationKey` from the URL and pass it as a request header. Two Pandino action hooks redirect to `/Ubives/AccountActor/` after accept/cancel operations. The AcceptInvitationLinkParamater form is overridden to mask password and passwordAgain fields with `type="password"`.
- Notable: The invitation acceptance flow is entirely anonymous (no authentication required). The URL structure carries the invitation key as a query parameter, and the axios interceptor ensures it reaches the backend on every request.

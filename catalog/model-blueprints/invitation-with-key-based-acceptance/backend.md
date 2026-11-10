## Backend guidance

### Generate the key with a secure random source

The key in the link must be random and unguessable. Generate it with a cryptographically secure random source, and make it long enough to resist guessing. Do not derive it from the email or a counter.

```java
String key = secureRandomAlphanumeric(32);
```

### Create invitations in a dedicated operation

Create the Invitation in a custom operation that sets the type, the email, an expiration, and the key. Send the email after the invitation is saved, so a failed save does not send a link.

### Check the key and the expiration on accept

On accept, load the invitation by its key, refuse the call if the key is unknown, and refuse it if the expiration has passed. Then branch on the invitation type: USER creates a user, ACCOUNT adds the existing account to the organization.

### Check the password confirmation in the operation

The accept operation checks that the password and its confirmation match before it creates anything. Report a mismatch as a field error: throw `ValidationException` (HTTP 400) with the attribute as location, not a business fault (422).

### Delete the invitation after acceptance

Delete the invitation in the same transaction that creates the user or the membership. A failure then rolls back the whole acceptance, and the link stays usable. This relies on the operation running in one transaction; verify that for the project's custom operation setup.

### Cancel only pending invitations

Cancel deletes the invitation. Refuse to cancel an invitation that was already accepted.

### Interceptors do not run here

Accept and cancel are custom operations. The platform fires interceptors only for built-in behaviour operations, so no interceptor and no write guard runs around a custom, MAPPED or script operation. Write permission checks, audit rows, notifications and side effects inside the `*CustomImplementation`.

### Keep the example services out of the platform

The example project places this logic in its own invitation service with an email component and a realm manager. Those classes are example project code, not platform API. Copy the sequence, not the names. The secure-random helper in the sample is also an example, not a platform call.

### Supersede a pending invitation on re-invite
When the inviter retries (typo, wrong role, lost link), delete the existing pending invitation for the same address inside the create operation, then create the new one. The old key is invalid as soon as the row is gone. Refuse the re-invite when the existing invitation is already verified, because the invitee has engaged and needs an explicit decision. Record the superseded invitation id in the audit entry, written in the same operation.

## Examples

### ubives

- Invitations are created by two custom operations, one per type. Both call one shared invitation service, so the email and the key generation live in one place.
- The accept operation is the only one with inline checks: it rejects a password mismatch before calling the service.
- Acceptance for a new user provisions the user in the organization's identity realm. Acceptance for an existing account adds an access entry for the organization.
- The invitation link carries the key as a query parameter, and the anonymous page reads it from the URL.

### mlszksz-platform
- The invite operation supersedes a pending invitation for the same email and refuses when a verified one exists. The service logs the audit entry with a superseded flag and the old invitation id.

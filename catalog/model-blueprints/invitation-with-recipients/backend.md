## Backend guidance

### Create the batch and its recipients in one operation

Create the Invitation and all its InvitationRecipient entities in one custom operation, so that one failure leaves no half-created batch. Check that the project's custom operation runs the DAO writes in one transaction; do not assume it. A failure then leaves no half-created batch.

### Store only the hash of each token

Generate a random verification token for each recipient. Store only a hash of it on the recipient. Send the plain token once, in the invitation email. Hash the incoming token the same way when it comes back.

```java
// Example project code; the hash helper and token generator are not platform API
String token = secureRandomToken();
recipient.setVerificationTokenHash(sha256(token));
recipient.setVerificationExpiresAt(now.plusDays(expiryDays));
```

### Send the email after the save

Send the invitation emails after the batch and its recipients are saved. A send failure must not hide a saved batch; log it and let an administrator resend.

### Check the window and the reuse flag on use

When a recipient's token comes back, look up the recipient by the hash of the token. Refuse it if the verification window has passed. Refuse it if the recipient was already used. Mark the recipient used only after the registration has succeeded.

### Keep the expiry in configuration

Read the number of days from configuration, not from a constant in code, so each deployment can choose its own window.

### Name the entry points for the actor

Batch creation and single-user invitation are two custom operations, each reached from its own actor's screen. Because interceptors never run for custom operations, each operation must itself check that the calling actor may invite, and into which organization and with which role. Both call one shared service that creates the recipients and sends the emails.

### Project services are not platform API

The example project uses its own invitation service, token utilities and email service. Those are example project code, not platform API. Copy the pattern and not the names.

## Examples

### mlszksz-platform

- A bulk operation on the admin dashboard parses a list of addresses and creates one invitation with one recipient per address. A single-user operation on the organization panel creates a one-recipient invitation.
- Each recipient gets a random token, stored as a SHA-256 hash, with an expiry read from configuration.
- The registration service looks up the recipient by the token hash, checks the expiry and the used flag, and marks it used after a successful registration.

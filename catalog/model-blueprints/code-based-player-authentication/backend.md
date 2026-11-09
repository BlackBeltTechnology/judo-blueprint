## Backend guidance

### Register and activate are custom operations

Register and activate are custom static operations on the Application transfer object. Interceptors do not run for them, so every rule must sit in the operation implementation itself.

- Register looks up the User by e-mail. If none exists it creates one; if one exists it updates the name when one is given. Either way it writes a new pending code, never a second user.
- Register generates the pending code with a secure random source, stores it on the User, and sends it by e-mail through a platform mail service inside the same operation.
- Activate looks up the User by e-mail and checks the pending code in the same query. On a match it clears the pending code and sets the active code.
- On any mismatch activate returns one generic fault, so the caller cannot tell an unknown e-mail from a wrong code.

### Keep the e-mail send out of the business change

A failed e-mail should not leave a half-registered user. Either send the e-mail after the transaction commits, or use a safe-failure wrapper so a send error is logged and the user row is still valid. See [[safe-failure-pattern]].

### Reset issues a new active code

The reset operation regenerates the active code on the User. It is an instance operation, so it can be called from the admin side as well as the player side. It must check that the caller may reset this user.

### Project code, not platform API

The example project implements these operations with its own user data-access class and mail service. Those names are project code. Copy the pattern, not the names.

## Examples

### trivia

- Register and activate are implemented as custom operation classes with injected user access and mail services.
- The e-mail body includes a privacy notice held in a constant.
- Register is idempotent per e-mail. Activate compares e-mail and pending code together.

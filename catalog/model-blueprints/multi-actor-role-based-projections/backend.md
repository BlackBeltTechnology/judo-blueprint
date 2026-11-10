## Backend guidance

Actor projections are read and written by the generated operations of each actor's transfer objects. Backend code adds behaviour in three places.

### Custom operations use the projection they serve

A custom operation on a restricted transfer object should check its input against that actor's rules. Do not rely on the admin view to enforce them. Custom operations are never intercepted, so the check belongs in the operation body or in a service it calls.

### Interceptors cover built-in operations only

An interceptor runs only on built-in operations. It may only throw InterceptorCallBusinessException. Use an interceptor for cross-cutting checks on built-in create, update and delete, and put the checks for custom operations in the operation itself.

### Shared logic lives in project services

A helper that reads the current user and filters by actor is project code, for example a service in the example project. It is not a platform API. Keep one such helper per project and call it from each restricted operation.

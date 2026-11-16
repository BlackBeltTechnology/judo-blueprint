## Backend guidance

The open and close operations are custom implementations, so the body is written in backend code.

### Custom operations are never intercepted

Interceptors fire only on built-in operations (create, update, delete, list and the like). A check that the entity can be opened or closed belongs in the operation body or in a project service it calls.

### Interceptors may only throw InterceptorCallBusinessException

If an interceptor is used for built-in create, update or delete, it may only throw InterceptorCallBusinessException. Do not throw other exceptions from it.

### Project helpers are example code

A helper that checks the window or records who opened it is project code, for example a service in the example project. It is not a platform API.

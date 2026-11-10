## Backend guidance

The capability operations are custom operations on the administrator's view of Capability. Interceptors never run for custom, mapped or script operations, so their rules live in the operation or in the service behind it.

### Operations are thin wrappers over one service

Create, update and toggle each call one master-data service. The operation class is a `*CustomImplementation` OSGi component (`@Component` with `service` set to the generated operation interface) that receives the service by injection and delegates. Both the service and the operation classes are project code, not platform API.

```java
public class ActivateToggleCustomImplementation implements ActivateToggleOperation {
    private final MasterDataService masterData;  // project service

    public Capability activateToggle(Capability capability) {
        return masterData.toggleCapabilityActive(capability);
    }
}
```

### Create at the dashboard, toggle on the instance

A creation operation belongs to the dashboard, because it has no instance yet. Toggle and update belong to the instance, because they act on one capability. Both groups call the same service, so the rules for a name stay in one place.

### Keep seed data in the initializer

Initial capabilities are created once at startup with the generated DAO (the DAO runs in a transaction context: a startup component must provide one). The initializer is project code; it is not a platform hook.

### Toggle changes visibility, not references

Setting isActive to false does not remove the association rows that point to the capability. Read paths that offer choices should filter on isActive; read paths that show existing tags should not.

### Name uniqueness is a service rule

The identifier is required, but the uniqueness check is project logic in the service. Check it before create and update, and report a field error when it fails: a `ValidationException` is HTTP 400 and a modeled fault is a business error. A custom operation that throws a modeled fault must declare it on the operation in the model.

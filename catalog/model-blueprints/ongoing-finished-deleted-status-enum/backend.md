## Backend guidance

The status drives behaviour in custom operations and in scheduled jobs. Both live in application code, and neither is covered by an interceptor.

### Put transitions in one service

Keep every status change in one service class. Custom operations and scheduled jobs both call it, so the rules are written once. The service is application code (an example name is `ActivityService`), not a platform class.

```java
public class ActivityService {
    public void finishExpired(LocalDate today) {
        // find ONGOING activities whose end date has passed, then set FINISHED
    }

    public void softDelete(Activity activity) {
        activity.setStatus(ActivityStatus.DELETED);
    }
}
```

### Check the current status inside the transition

Custom (SDK-implemented), mapped and script operations never run through interceptors, so a transition must check the current status itself before it changes it. A guard written as an interceptor would not protect a custom operation.

### Built-in updates can be guarded

Built-in create and update operations do run interceptors. If a rule must hold for every built-in write to the status, an interceptor can enforce it, but it may throw only `InterceptorCallBusinessException`, and it should not be the only check because it never sees the custom operations and the job.

### Filter by status and date in the query

Scheduled work selects activities by status and by a date range, for example ONGOING activities whose end date is before today. Filtering in the query keeps the job from loading finished activities.

### Scheduled jobs use the same service

A background job is an OSGi component that runs on a schedule (see [[osgi-scheduled-background-jobs]]). Scheduled execution happens outside the request-scoped transaction context, so database work in the job needs its own context (see the Quartz scheduled job practice). It calls the same transition service as the operations, so an activity finished by the job follows the same rules as one finished by a user.

### Children follow the owner

A tracked activity takes its initial status from its owner when it is created. When the owner changes status, the children must be updated in the same service call, not left to a later job.

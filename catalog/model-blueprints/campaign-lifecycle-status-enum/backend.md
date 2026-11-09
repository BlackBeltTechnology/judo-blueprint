## Backend guidance

The status drives behaviour in custom operations and in scheduled jobs. Both live in project code, and neither is covered by an interceptor.

### Put transitions in one service

Keep every status change in one service class. Custom operations and scheduled jobs both call it, so the rules are written once. The service is project code (an example name is `CampaignService`), not a platform class.

```java
public class CampaignService {
    public void finishExpired(LocalDate today) {
        // find ONGOING campaigns whose end date has passed, then set FINISHED
    }

    public void softDelete(Campaign campaign) {
        campaign.setStatus(CampaignStatus.DELETED);
    }
}
```

### Check the current status inside the transition

Custom operations do not run through interceptors, so a transition must check the current status itself before it changes it. A guard written as an interceptor would not protect a custom operation.

### Built-in updates can be guarded

Built-in create and update operations do run interceptors. If a rule must hold for every write to the status, an interceptor can enforce it, but it may throw only `InterceptorCallBusinessException` and it should not be the only check.

### Filter by status and date in the query

Scheduled work selects campaigns by status and by a date range, for example ONGOING campaigns whose end date is before today. Filtering in the query keeps the job from loading finished campaigns.

### Scheduled jobs use the same service

A background job is an OSGi component that runs on a schedule. It calls the same transition service as the operations, so a campaign finished by the job follows the same rules as one finished by a user.

### Children follow the owner

A tracked campaign takes its initial status from its owner when it is created. When the owner changes status, the children must be updated in the same service call, not left to a later job.

---
id: "multi-actor-role-based-projections"
title: "Multi-Actor Role-Based Transfer Object Projections"
score: 41.7
usage_count: 5
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - reserve-app
  - viterra_demo
  - doors-model
  - ams-model
  - skillmatrix-model
---
## Description

A pattern where the same underlying entity types are exposed through multiple role-specific transfer object projections, one per actor type. Each actor sees a tailored view of the domain: some fields are omitted (e.g., partners do not see internal logistics fields), some are read-only, and some are denormalized into display strings (e.g., `projectAsString` instead of a project relation). The Role enum defines all possible roles (e.g., PARTNER, LOGISTICIAN, DOORMAN, READ_ONLY, ADMIN), and each role maps to a dedicated ActorType. The User entity carries a `role` attribute typed to this enum, and associations to role-relevant entities (e.g., partner association for PARTNER role users, company association for internal users, projects for scoped access).

Transfer objects follow a naming convention: `<EntityName>For<RoleName>` (e.g., ReservationForPartner, ProjectForPartner, GateForPartner) or `<RoleName><EntityName>Transfer` (e.g., PartnerOpenReportTransfer, PartnerClosedReportTransfer). The admin actor gets the full entity view while restricted roles get filtered projections with only the attributes relevant to their workflow. User TOs similarly follow a per-role pattern: AdminUser, PartnerUser, LogisticianUser, DoormanUser, ReadonlyUser -- all projecting the same User entity with role-appropriate fields. In some projects, different actor packages contain completely different transfer objects for the same entity (e.g., admin::Company vs employee::Contract mapping the same underlying entities with different field sets and operations). Some projects use a principal-based Employee actor with a self-filtering `isActiveExpression` for authentication-aware data access. In some projects, the Manager actor uses `isActiveExpression` based on a relation count (e.g., `self.subordinates!count() > 0`) to restrict access to users who have subordinates.

In some projects, the Partner actor uses derived access expressions with `getVariable("ACTOR", "email")` to filter data to only the records belonging to the logged-in user, creating a self-service portal view.

In some projects (e.g., kozut-eugyfel-client), the actors represent internal organizational roles (Admin, Munkatars/Worker, external e-service application) rather than customer-facing roles, and the same Bejelentes (report/ticket) entity is projected differently per actor: the Admin sees a summary list with status, the Munkatars sees a full detail view with forwarding/close/comment operations and permission guard attributes, and the external application sees only a creation view.

In some projects (e.g., skillmatrix-model), the actors correspond to boolean role flags on the User entity (isActiveAdmin, isActiveHREmployee, isActiveProfessional) rather than a Role enum. Each actor package (admin, hrEmployee, professional, manager) contains completely different TOs for the same entities, with the admin seeing user management views, the HR employee seeing competence/skill management, the professional seeing personal skill self-assessment, and the manager seeing subordinate skill approval.

In some projects, the actor types are bound directly to entity subtypes via `actorType` references on the entity definition. The abstract User entity has concrete subtypes each carrying an `actorType` reference to their corresponding ActorType, and the actors share entity-level access points via a central Admin actor.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

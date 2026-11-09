---
id: "competence-skill-matrix-cluster"
title: "Competence/Skill Matrix Entity Cluster with Levels and Approval"
score: 30.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - skillmatrix-model
---
## Description

An entity cluster for managing employee competences and skill assessments. The core pattern consists of:

- **Competence** -- a named capability area (e.g., "Java Programming", "Project Management") with a `strategic` boolean flag indicating organizational importance, an `active` flag for soft-disable, and many-to-many associations to Tags for classification.
- **SkillLevel** -- a reference data entity defining proficiency tiers (e.g., Beginner, Intermediate, Advanced, Expert) with a `name` and numeric `score` for quantitative comparison.
- **Skill** -- a junction entity linking a User to a Competence with two SkillLevel references: `requestedLevel` (self-assessed by the professional) and `approvedLevel` (confirmed by a manager). A derived `approved` boolean computes whether the two levels match. An `approve` operation copies the requested level to the approved level.
- **SkillTarget** -- a goal entity within a TrainingPlan, linking a Competence to a target SkillLevel with a `deadline` date and `completed` boolean. Represents what skill level an employee should achieve by a given date.
- **User** -- the employee entity, carrying skills (0..* ASSOC), trainingPlans (0..* COMPOSITION), and operations for bulk approval and training plan creation.

The pattern supports a three-actor workflow:
1. **Professional** (employee) -- requests skill levels via self-assessment
2. **Manager** -- reviews and approves requested levels, creates training plans with skill targets
3. **HR Employee** -- administers competences, tags, skill levels, and organizational units

Derived attributes flatten navigation for display: `competenceName`, `approvedLevelName`, `requestedLevelName`, `userFullName`, `unitName`, `competenceScore` on the Skill entity.

This pattern is characteristic of HR/talent management systems where skill gap analysis, training planning, and competency mapping are core business processes.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

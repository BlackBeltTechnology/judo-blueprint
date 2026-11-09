---
id: "work-status-lifecycle-enum"
title: "Work Status Lifecycle Enum (Not Started/In Progress/Done/Won't Fix)"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A four-state work/task lifecycle enumeration with members: NOT_STARTED, IN_PROGRESS, DONE, and WONT_FIX. This models entities that track repair or maintenance work items: they begin as NOT_STARTED, transition to IN_PROGRESS when work begins, and end at either DONE (completed) or WONT_FIX (abandoned/deferred). The WONT_FIX terminal state distinguishes this from simpler lifecycle enums by acknowledging that not all work items reach completion. Used by both JobSheet and WorkReport entities as their workStatus attribute.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

---
id: "risk-level-enum"
title: "Risk Level Enum (LOW/MEDIUM/HIGH)"
score: 38.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - itracker
---
## Description

A three-level risk classification enumeration with members LOW, MEDIUM, and HIGH. This pattern models a simple ordinal risk assessment scale used as an attribute on domain entities to categorize items by their risk exposure. The enum is intentionally minimal -- three levels provide enough granularity for quick triage and dashboard filtering without overcomplicating the assessment process.

This pattern is suitable for project management, initiative tracking, issue triage, procurement risk assessment, compliance scoring, and any domain where items need a simple risk categorization for prioritization and reporting.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

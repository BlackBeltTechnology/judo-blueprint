---
id: "environment-enum"
title: "Environment Enum (DEV/TEST/PROD Deployment Stages)"
score: 36.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - InterfaceRegister
---
## Description

An enumeration representing deployment environment stages, typically with three members: DEV (development), TEST (testing/staging), and PROD (production). This is a standard software lifecycle classification used to categorize application instances, server deployments, or configuration sets by their target environment. The enum enables filtering and grouping resources by environment in enterprise architecture and operations management contexts.

This enum is typically used as a required attribute on deployment-related entities (e.g., ApplicationInstance, Server, DeploymentItem) to indicate which environment a particular resource belongs to.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

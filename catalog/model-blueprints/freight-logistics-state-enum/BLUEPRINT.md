---
id: freight-logistics-state-enum
title: Freight/Logistics Lifecycle State Enum
description: "A multi-state lifecycle enumeration for freight, delivery, or logistics reservation workflows."
aliases: []
keywords: [freight, logistics, lifecycle, state, enum]
tags: ["domain:model", "layer:model", "project:reserve-app", "status:single-project"]
category: pattern
status: single-project
projects: [reserve-app]
evidence: ["reserve-app:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

A multi-state lifecycle enumeration for freight, delivery, or logistics reservation workflows. The enum models the full journey of a shipment or freight booking from initial creation through completion: NOT_SUBMITTED (draft/created but not sent), SUBMITTED (sent for review), APPROVED (accepted by logistics), REJECTED (declined), SUSPENDED (temporarily halted), ARRIVED (physically arrived at facility), FINISHED (unloading/processing complete), plus delay states (DELAYED_ARRIVAL, DELAYED_UNLOADING) for tracking schedule deviations. This is significantly richer than simple ACTIVE/DELETED/EXPIRED reservation status enums, reflecting the complex multi-party handoffs in logistics workflows where a partner submits a reservation, a logistician approves or rejects it, and a doorman tracks arrival and completion.

The enum supports suspension by either party (partner or logistician) via separate suspendedByPartner and suspendedByLogistician relations on the reservation entity, enabling tracking of who initiated the hold.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

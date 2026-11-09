---
id: "application-vendor-integration-registry"
title: "Application-Vendor Integration Registry (Enterprise Architecture)"
score: 36.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - InterfaceRegister
---
## Description

An enterprise integration registry entity cluster for tracking applications, their vendors, connections between applications, and deployment instances. The core entities are:

- **Application** -- a software application with id, name, version, category (enum: CRM, DMS, IMS, etc.), and a required association to its Vendor
- **Vendor** -- the company that provides/develops the application, with id, name, and address
- **HighLevelConnection** -- a business-level connection between two applications (sender and receiver), describing data flow with a name, description, periodicity (enum: ADHOC, HOURLY, DAILY, etc.), and associations to BusinessDataType and Brand entities for classification
- **ConnectionDefinition** -- a technical-level connection specification linking a HighLevelConnection to an InterfaceSpecification, with direction of data transmission, periodicity details, and optional client/server Application references
- **ApplicationInstance** -- a deployed instance of an Application in a specific Environment (DEV, TEST, PROD)
- **DeploymentItem** -- a deployment artifact associated with an ApplicationInstance
- **Server** -- a server hosting applications, with composed IP addresses (IPV4Address, IPV6Address)
- **ProvidedInterface** -- links an InterfaceSpecification to network addressing (port, IPv4/IPv6 address)
- **ClientInterface** -- links an InterfaceSpecification to a client-side endpoint
- **ConcreteConnection** -- connects a ClientInterface to a ProvidedInterface through a ConnectionDefinition, with an optional connect string

This cluster models the full enterprise integration landscape: what applications exist, who provides them, how they connect at both business and technical levels, and where they are deployed. The HighLevelConnection provides business stakeholders with an overview, while ConnectionDefinition, ProvidedInterface, ClientInterface, and ConcreteConnection provide technical details.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

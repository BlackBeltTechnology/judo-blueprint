---
id: "standard-type-and-measure-library"
title: "Standard Type and Measure Library (Shared Type System)"
score: 46.0
usage_count: 8
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - bhs-global-operation
  - viterra_demo
  - InterfaceRegister
  - mjsz
  - sanctuary-backend
  - doors-model
  - ams-model
  - skillmatrix-model
---
## Description

A standardized type system and comprehensive SI measurement unit library embedded in a JUDO model. The structure consists of:

- **types package** -- defines primitive data types: numeric types (Long, Integer, Double, Float) with specific precision/scale, string types (String, Phone, Text, URL, Email) with varying maxLength constraints, a Boolean type, a Date type, a Timestamp type, and a Time type. Some projects add domain-specific string types (e.g., IPV4Address, IPV6Address, FinancialCode, LegalCode, CompanyCode, DivisionCode, ContractTypeTemplate, ContractTemplate, SignedContract, CampaignDocument).
- **measures package** -- defines physical measure categories (Mass, Length, Time, Temperature, Area, Volume, Velocity, Acceleration, Momentum, Force, Work, Power, Frequency, Pressure, Density, ElectricCurrent, ThermodynamicTemperature, AmountOfSubstance, LuminousIntensity, ElectricCharge, ElectricPotential, Capacitance, ElectricalResistance, ElectricalConductance, MagneticFlux, MagneticFluxDensity, Inductance, Illuminance) with a full set of SI units (79 total) including metric prefixes (milli, centi, deci, kilo, mega, etc.) and derived units (km/h, m/s, kg/m3, etc.).

This pattern provides a standardized type vocabulary across an organization's JUDO projects, ensuring consistent precision, scale, string length constraints, and measurement units. In some projects (bhs-global-operation) it exists as a standalone type-only model for import. In others (viterra_demo, InterfaceRegister, mjsz, sanctuary-backend, doors-model, ams-model, kozut-eugyfel-client, skillmatrix-model) it is embedded directly within the application model alongside domain entities. The type and measure definitions are virtually identical across projects, indicating a shared organizational standard.

The string types include domain-aware subtypes: Phone (maxLength: 20) for phone numbers, Email (maxLength: 255) for email addresses, URL (maxLength: 1024) for web addresses, and Text (maxLength: 250, 1000, or 2000) for short text fields, in addition to a general-purpose String (maxLength: 255).

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

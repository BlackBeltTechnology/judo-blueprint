---
id: "error-code-enum-pattern"
title: "Error Code Enumeration for Operation Faults"
domain: "model"
category: "enum"
score: 54.7
usage_count: 4
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - park-here
  - indamedia-adtrack
  - judo-partner
---
## Description

Operations that can fail use a dedicated Error transfer object (unmapped) containing a message string and a typed error code enumeration. The error code enum lists all possible domain-specific failure reasons, enabling structured error handling on the client side.

## Structure

- Unmapped transfer object `Error` or `BusinessError` with:
  - `message: String` (optional or required, human-readable)
  - `code/errorCode: ErrorCode` (required, typed enum)
- ErrorCode enum defines domain-specific error conditions
- Error is used as the fault type for operations: `fault: Error (1..1)`
- Error enum placed in the actor package (not entities) when actor-specific

## Examples

### Trivia
`player::Error` has `message` (String, optional) and `code` (ErrorCode, required). `ErrorCode` enum has 5 members: `INVALID_CODE`, `CONTEST_NOT_OPEN`, `TEST_NOT_STARTED`, `TEST_ALREADY_STARTED`, `TEST_CLOSED`. Used as fault type for `enter`, `submit`, `start`, and `activate` operations.

### ParkHere
`BusinessError` transfer has `message` (String, required) and `errorCode` (ErrorCode, required). `ErrorCode` enum has 8 members: `PERMISSION_DENIED`, `USER_NOT_FOUND`, `MISSING_REQUIRED_DATA`, `NOT_VALID_DATA`, `RESERVATION_NOT_FOUND`, `TOO_MANY_RESERVATION`, `CAR_NOT_FOUND`, `CONFIGURATION_NOT_FOUND`. Used as fault type across 20+ operations including `favoriteCar`, `deleteCar`, `configuration`, `createDoorman`, `deleteHoliday`, etc.

### IndamediaAdTrack
`BusinessError` transfer used as the single fault type for all 17 operations. `ErrorCode` enum has 12 members spanning 4 categories: entity-not-found (`CLIENT_NOT_FOUND`, `USER_NOT_FOUND`, `ACCOUNT_NOT_FOUND`, `CAMPAIGN_NOT_FOUND`, `CREDENTIAL_NOT_FOUND`, `TRACKED_CAMPAIGN_NOT_FOUND`), authorization (`PERMISSION_DENIED`), configuration (`CREDENTIAL_NOT_SET`), and platform integration (`CONNECTION_FAILD`, `TRACKED_CAMPAIGN_UNFETCHABLE`, `PLATFORM_NOT_SUPPORTED`, `PLATFORM_NOT_IMPLEMENTED`).

### judo-partner
`ValidationErrorCode` enum with 9 members classifying partner validation failures: `NON_HU_TAX_ID`, `INVALID_TAX_ID`, `TAX_ID_SUFFIX_ERROR`, `UNDER_LIQUIDATION`, `UNDER_DISSOLUTION`, `NAME_MISMATCH`, `MISSING_TAX_ID`, `DUPLICATE_TAX_ID`, `COMMUNICATION_ERROR`. Used on both `Partner.validationError` and `ImportPartner.validationError` to record validation results from NAV tax authority queries.

## Trade-offs

- Pros: Typed error codes enable structured client-side error handling, self-documenting API errors
- Cons: Adding new error conditions requires enum changes, error codes must be kept in sync with operation logic
- Prefer when: Operations need to communicate specific failure reasons to clients

## Related Patterns

- [unmapped-transfer-dto](unmapped-transfer-dto.md)
- [enum-state-machine](enum-state-machine.md)

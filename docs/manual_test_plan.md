# Manual Test Plan - ExpandTesting Notes App

## Purpose

Validate the Notes application manually across UI, API, and UI/API synchronization before and alongside automation.

## Scope

- UI login, logout, create note, edit note, delete note, and validation errors.
- API authentication, GET notes, create note, update note, delete note, and negative responses.
- Hybrid checks where UI-created data is available through API and API changes are visible in UI.
- Basic performance checks for API response time and UI DOM readiness.

## Application Under Test

- UI: https://practice.expandtesting.com/notes/app
- API docs: https://practice.expandtesting.com/notes/api/api-docs/

## Functional Requirements

| Req ID | Description |
| --- | --- |
| FR-01 | UI login should work with valid credentials. |
| FR-02 | User should be able to create a note via UI. |
| FR-03 | UI-created note should appear instantly in the notes list. |
| FR-04 | API GET /notes should return the user's note list. |
| FR-05 | UI-created note should appear in API response. |
| FR-06 | User should be able to delete a note via API. |
| FR-07 | API-deleted note should disappear from UI. |
| FR-08 | API GET /notes response time should be less than 2 seconds. |
| FR-09 | Negative UI and API scenarios should return clear validation/errors. |
| FR-10 | User should be able to edit notes via UI and API. |

## Test Strategy

- Execute structured UI validation in Chrome.
- Execute API validation with authenticated and unauthenticated requests.
- Compare UI and API data using title and description pairs when UI does not expose a note ID.
- Log defects with exact data, request payload, response body, and screenshots.
- Repeat flaky UI failures after checking locator stability and page timing.

## Entry Criteria

- Test account is available in `.env`.
- UI and API endpoints are reachable.
- Browser and network are stable.
- Test data can be created and deleted.

## Exit Criteria

- All critical scenarios pass.
- No blocker or critical defects remain open.
- Automation suite runs with reports generated.
- RTM confirms every requirement has at least one scenario and test case.

## Risks

- Shared test account data can cause false positives if old notes are not cleaned up.
- Network latency can affect UI/API synchronization timing.
- UI locator changes can break Selenium tests before business behavior changes.

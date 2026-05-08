# Test Scenarios, Test Cases, and RTM

## Test Scenarios

| Scenario ID | Requirement | Scenario |
| --- | --- | --- |
| TS-01 | FR-01 | Validate successful UI login with valid credentials. |
| TS-02 | FR-09 | Validate failed UI login with invalid credentials. |
| TS-03 | FR-02, FR-03 | Validate note creation through UI and immediate list visibility. |
| TS-04 | FR-10 | Validate note editing through UI. |
| TS-05 | FR-04, FR-08 | Validate GET /notes returns notes within the response-time threshold. |
| TS-06 | FR-02 | Validate note creation through API. |
| TS-07 | FR-10 | Validate note update through API. |
| TS-08 | FR-06 | Validate note deletion through API. |
| TS-09 | FR-05 | Validate UI-created note appears in API response. |
| TS-10 | FR-07 | Validate API-deleted note disappears from UI. |
| TS-11 | FR-09 | Validate UI note form rejects missing required fields. |
| TS-12 | FR-09 | Validate API rejects unauthorized and invalid requests. |

## Test Cases

| Test Case ID | Scenario | Steps | Expected Result | Automated Test |
| --- | --- | --- | --- | --- |
| TC-UI-01 | TS-01 | Open login page, enter valid email/password, submit. | Notes page is displayed with Add Note control. | `tests/ui/test_login.py::test_valid_login` |
| TC-UI-02 | TS-02 | Open login page, enter invalid credentials, submit. | Error message is shown. | `tests/ui/test_login.py::test_invalid_login` |
| TC-UI-03 | TS-03 | Login, create note with category/title/description, save. | Note appears in UI without manual reload. | `tests/ui/test_notes.py::test_create_note` |
| TC-UI-04 | TS-04 | Login, create note, edit title/description/category/status. | Updated note appears and old title is absent. | `tests/ui/test_notes.py::test_edit_note` |
| TC-UI-05 | TS-11 | Login, open note form, omit title, save. | Required-field validation is displayed. | `tests/ui/test_note_validation.py::test_create_note_without_title` |
| TC-API-01 | TS-05 | Login through API, call GET /notes. | Status 200, note list returned, response under 2 seconds. | `tests/api/test_notes_api.py::test_get_notes_response_time` |
| TC-API-02 | TS-06 | Login through API, POST /notes with valid payload. | Status 200 and returned title matches request. | `tests/api/test_notes_api.py::test_create_note_api` |
| TC-API-03 | TS-07 | Create note through API, PUT /notes/{id}. | Status 200 and updated fields match request. | `tests/api/test_notes_api.py::test_update_note_api` |
| TC-API-04 | TS-08 | Create note through API, DELETE /notes/{id}. | Status 200/204 and note is deleted. | `tests/api/test_notes_api.py::test_delete_note_api` |
| TC-API-05 | TS-12 | Call POST/GET notes without token. | Status 401/403. | `tests/api/test_notes_api.py::test_create_note_without_token`, `test_get_notes_without_token_api` |
| TC-API-06 | TS-12 | Create note without title or delete invalid note ID. | API returns validation/not-found status. | `tests/api/test_notes_api.py::test_create_note_without_title_api`, `test_delete_note_with_invalid_id_api` |
| TC-E2E-01 | TS-09 | Create note in UI, call GET /notes, compare title and description. | UI note exists in API with matching fields. | `tests/e2e/test_ui_api_sync.py::test_create_note_ui_validate_api` |
| TC-E2E-02 | TS-10 | Create note through API, delete via API, refresh UI. | Deleted note no longer appears in UI. | `tests/e2e/test_ui_api_sync.py::test_delete_note_api_validate_ui` |
| TC-E2E-03 | TS-04, TS-09 | Edit note in UI, call GET /notes, compare updated fields. | API returns updated title and description. | `tests/e2e/test_ui_api_sync.py::test_edit_note_ui_validate_api` |
| TC-E2E-04 | TS-04, TS-07 | Edit note through API, refresh UI. | UI displays updated note title. | `tests/e2e/test_ui_api_sync.py::test_edit_note_api_validate_ui` |

## Requirement Traceability Matrix

| Req ID | Scenario IDs | Test Case IDs |
| --- | --- | --- |
| FR-01 | TS-01 | TC-UI-01 |
| FR-02 | TS-03, TS-06 | TC-UI-03, TC-API-02 |
| FR-03 | TS-03 | TC-UI-03 |
| FR-04 | TS-05 | TC-API-01 |
| FR-05 | TS-09 | TC-E2E-01, TC-E2E-03 |
| FR-06 | TS-08 | TC-API-04 |
| FR-07 | TS-10 | TC-E2E-02 |
| FR-08 | TS-05 | TC-API-01 |
| FR-09 | TS-02, TS-11, TS-12 | TC-UI-02, TC-UI-05, TC-API-05, TC-API-06 |
| FR-10 | TS-04, TS-07 | TC-UI-04, TC-API-03, TC-E2E-03, TC-E2E-04 |

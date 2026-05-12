import pytest
import uuid

import os
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

from config.environment import config

from pages.login_page import LoginPage

from pages.notes_page import NotesPage

from api.auth_api import AuthAPI

from api.notes_api import NotesAPI

from utils.logger import get_logger
from utils.performance_logger import PerformanceLogger


logger_obj = get_logger()

load_dotenv()


def get_api_client():

    auth_api = AuthAPI()

    response = auth_api.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

    token = response.json()["data"]["token"]

    return NotesAPI(token)


def ui_login(driver):

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)

    login_page.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

@pytest.mark.e2e
def test_create_note_ui_validate_api(driver):

    ui_login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"UI_API_{unique_id}"

    description = (
        "Created via UI validated via API"
    )

    # create note in UI
    notes_page.create_note(
        title,
        description
    )

    # fetch notes via API
    notes_api = get_api_client()

    response = notes_api.get_notes()

    assert response.status_code == 200

    notes_data = response.json()["data"]

    matching_note = next(
        (
            note for note in notes_data
            if note["title"] == title
            and note["description"] == description
        ),
        None
    )

    assert matching_note is not None

@pytest.mark.e2e
def test_create_note_api_validate_ui(driver):

    ui_login(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"API_UI_{unique_id}"

    description = (
        "Created via API validated via UI"
    )

    # create note via API
    notes_api = get_api_client()

    response = notes_api.create_note(
        title,
        description
    )

    logger_obj.info(
        f"API Create Response Status: {response.status_code}"
    )

    logger_obj.info(
        f"API Create Response Body: {response.text}"
    )

    assert response.status_code == 200, \
        f"API create failed with {response.status_code}: {response.text}"

    # refresh UI
    driver.refresh()

    notes_page = NotesPage(driver)

    assert notes_page.is_note_created(title)

@pytest.mark.e2e
def test_delete_note_ui_validate_api(driver):

    ui_login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"DELETE_UI_API_{unique_id}"

    notes_page.create_note(
        title,
        "Delete validation"
    )

    notes_api = get_api_client()

    notes_before = (
        notes_api.get_notes()
        .json()["data"]
    )

    created_note = next(
        (note for note in notes_before
        if note["title"] == title),
        None
    )

    assert created_note is not None, \
        f"Note '{title}' not found in API response"

    notes_page.delete_note_by_title(title)

    notes_after = (
        notes_api.get_notes()
        .json()["data"]
    )

    titles = [
        note["title"]
        for note in notes_after
    ]

    assert title not in titles

@pytest.mark.e2e
def test_delete_note_api_validate_ui(driver):

    ui_login(driver)

    notes_api = get_api_client()

    unique_id = str(uuid.uuid4())[:8]

    title = f"API_DELETE_{unique_id}"

    response = notes_api.create_note(
        title,
        "API delete"
    )

    # Handle both response formats
    response_json = response.json()

    if "data" in response_json:
        note_data = response_json["data"]
    else:
        note_data = response_json

    note_id = note_data.get("id")

    assert note_id is not None, \
        f"Could not extract note ID from response: {response_json}"

    driver.refresh()

    notes_page = NotesPage(driver)

    assert notes_page.is_note_created(title)

    notes_api.delete_note(note_id)

    driver.refresh()

    WebDriverWait(driver, 10).until(
        lambda d:
        title.lower()
        not in d.page_source.lower()
    )

    assert not notes_page.is_note_created(title)


@pytest.mark.e2e
def test_edit_note_ui_validate_api(driver):

    ui_login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"EDIT_UI_API_{unique_id}"

    updated_title = f"EDITED_UI_API_{unique_id}"

    updated_description = "UI edit validated through API"

    notes_page.create_note(
        title,
        "Original UI note"
    )

    notes_page.edit_note_by_title(
        title,
        updated_title,
        updated_description,
        category="Work",
        completed=True
    )

    notes_api = get_api_client()

    notes_data = notes_api.get_notes().json()["data"]

    matching_note = next(
        (
            note for note in notes_data
            if note["title"] == updated_title
            and note["description"] == updated_description
        ),
        None
    )

    assert matching_note is not None


@pytest.mark.e2e
def test_edit_note_api_validate_ui(driver):

    ui_login(driver)

    notes_api = get_api_client()

    unique_id = str(uuid.uuid4())[:8]

    title = f"EDIT_API_UI_{unique_id}"

    response = notes_api.create_note(
        title,
        "Original API note"
    )

    response_json = response.json()

    note_data = response_json.get(
        "data",
        response_json
    )

    note_id = note_data.get("id")

    assert note_id is not None

    updated_title = f"EDITED_API_UI_{unique_id}"

    notes_api.update_note(
        note_id,
        updated_title,
        "API edit validated through UI",
        category="Work",
        completed=True
    )

    driver.refresh()

    notes_page = NotesPage(driver)

    assert notes_page.is_note_created(updated_title)

@pytest.mark.flaky(reruns=2)
@pytest.mark.e2e
def test_multiple_notes_ui_api_sync(driver):

    ui_login(driver)

    notes_page = NotesPage(driver)

    titles = []

    for i in range(3):

        unique_id = str(uuid.uuid4())[:8]

        title = f"MULTI_{unique_id}"

        titles.append(title)

        notes_page.create_note(
            title,
            f"Description {i}"
        )

        assert notes_page.is_note_created(title)

    notes_api = get_api_client()

    for _ in range(5):

        response = notes_api.get_notes()

        api_titles = [
            note["title"]
            for note in response.json()["data"]
        ]

        if all(
            title in api_titles
            for title in titles
        ):

            break

    else:

        pytest.fail(
            "All notes not found in API"
        )

    for title in titles:

        assert title in api_titles


@pytest.mark.e2e
@pytest.mark.performance
def test_notes_ui_dom_ready_under_threshold(driver):

    ui_login(driver)

    timing = driver.execute_script(
        "return window.performance.timing"
    )

    dom_ready_seconds = (
        timing["domContentLoadedEventEnd"]
        - timing["navigationStart"]
    ) / 1000

    PerformanceLogger.record(
        "test_notes_ui_dom_ready_under_threshold",
        "UI DOM ready",
        dom_ready_seconds,
        "pass" if dom_ready_seconds < 5 else "fail"
    )

    assert dom_ready_seconds < 5

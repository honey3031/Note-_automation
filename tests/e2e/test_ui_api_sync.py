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

    titles = [
        note["title"]
        for note in notes_data
    ]

    assert title in titles

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

    notes_api = get_api_client()

    response = notes_api.get_notes()

    api_titles = [
        note["title"]
        for note in response.json()["data"]
    ]

    for title in titles:

        assert title in api_titles

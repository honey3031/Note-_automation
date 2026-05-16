import pytest
import uuid

import os

from dotenv import load_dotenv

from api.auth_api import AuthAPI

from api.notes_api import NotesAPI

from utils.logger import get_logger
from utils.performance_logger import PerformanceLogger
from mcp.test_data_generator import (
    AITestDataGenerator
)

logger = get_logger()

load_dotenv()


def get_token():

    auth_api = AuthAPI()

    response = auth_api.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

    assert response.status_code == 200

    token = response.json()["data"]["token"]

    return token



@pytest.mark.api
def test_create_note_api():

    token = get_token()

    notes_api = NotesAPI(token)

    ai_data = (
        AITestDataGenerator
        .generate_note()
    )

    print(
        f"\nAI GENERATED DATA:\n"
        f"{ai_data}\n"
    )

    title = ai_data[:30]

    description = ai_data

    response = notes_api.create_note(
        title,
        description
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["data"]["title"]
        == title
    )

@pytest.mark.api
def test_delete_note_api():

    token = get_token()

    notes_api = NotesAPI(token)

    unique_id = str(uuid.uuid4())[:8]

    title = f"Delete API {unique_id}"

    create_response = notes_api.create_note(
        title,
        "Delete test"
    )

    # Handle both response formats
    response_json = create_response.json()

    if "data" in response_json:
        note_data = response_json["data"]
    else:
        note_data = response_json

    note_id = note_data.get("id")

    assert note_id is not None, \
        f"Could not extract note ID from response: {response_json}"

    delete_response = (
        notes_api.delete_note(note_id)
    )

    logger.info(
        f"Delete response status: {delete_response.status_code}"
    )

    assert delete_response.status_code in [200, 204], \
        f"Delete failed with status {delete_response.status_code}: {delete_response.text}"


@pytest.mark.api
def test_update_note_api():

    token = get_token()

    notes_api = NotesAPI(token)

    unique_id = str(uuid.uuid4())[:8]

    title = f"API Edit {unique_id}"

    create_response = notes_api.create_note(
        title,
        "Original API note",
        category="Home"
    )

    response_json = create_response.json()

    note_data = response_json.get(
        "data",
        response_json
    )

    note_id = note_data.get("id")

    assert note_id is not None, \
        f"Could not extract note ID from response: {response_json}"

    updated_title = f"API Edited {unique_id}"

    update_response = notes_api.update_note(
        note_id,
        updated_title,
        "Updated API note",
        category="Work",
        completed=True
    )

    assert update_response.status_code == 200, \
        f"Update failed: {update_response.text}"

    updated_data = update_response.json().get(
        "data",
        update_response.json()
    )

    assert updated_data.get("title") == updated_title

    assert updated_data.get("description") == "Updated API note"



@pytest.mark.api
def test_create_note_without_token():

    import requests

    from config.environment import config

    endpoint = f"{config.api_url}/notes"

    payload = {
        "title": "Unauthorized",
        "description": "Should fail"
    }

    response = requests.post(
        endpoint,
        json=payload
    )

    assert response.status_code in [401, 403]

@pytest.mark.api
def test_create_note_without_title_api():

    token = get_token()

    notes_api = NotesAPI(token)

    response = notes_api.create_note(
        "",
        "Missing title"
    )

    assert response.status_code == 400


@pytest.mark.api
def test_get_notes_without_token_api():

    import requests

    from config.environment import config

    response = requests.get(
        f"{config.api_url}/notes"
    )

    assert response.status_code in [401, 403]


@pytest.mark.api
def test_delete_note_with_invalid_id_api():

    token = get_token()

    notes_api = NotesAPI(token)

    response = notes_api.delete_note(
        "invalid-note-id"
    )

    assert response.status_code in [400, 404]

@pytest.mark.api
@pytest.mark.performance
def test_get_notes_response_time():

    token = get_token()

    notes_api = NotesAPI(token)

    response = notes_api.get_notes()

    elapsed = response.elapsed.total_seconds()

    PerformanceLogger.record(
        "test_get_notes_response_time",
        "GET /notes response",
        elapsed,
        "pass" if elapsed < 2 else "fail"
    )

    assert elapsed < 2

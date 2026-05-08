import pytest
import uuid

import os

from dotenv import load_dotenv

from api.auth_api import AuthAPI

from api.notes_api import NotesAPI

from utils.logger import get_logger


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

    unique_id = str(uuid.uuid4())[:8]

    title = f"API Note {unique_id}"

    response = notes_api.create_note(
        title,
        "Created from API"
    )

    # Log response for debugging
    logger.info(f"Response Status: {response.status_code}")
    
    logger.info(f"Response Body: {response.text}")

    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}. Response: {response.text}"

    response_data = response.json()

    # Handle both 'data' wrapper and direct object
    if "data" in response_data:
        actual_data = response_data["data"]
    else:
        actual_data = response_data

    assert (
        actual_data.get("title")
        == title
    ), f"Title mismatch. Expected {title}, got {actual_data.get('title')}"


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
@pytest.mark.performance
def test_get_notes_response_time():

    token = get_token()

    notes_api = NotesAPI(token)

    response = notes_api.get_notes()

    assert response.elapsed.total_seconds() < 2
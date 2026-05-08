import pytest
import uuid

import os

from dotenv import load_dotenv

from config.environment import config

from pages.login_page import LoginPage

from pages.notes_page import NotesPage


load_dotenv()


def login(driver):

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)

    login_page.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

@pytest.mark.ui
def test_create_note(driver):

    login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"Automation Note {unique_id}"

    description = "Created by Selenium automation"

    notes_page.create_note(
        title,
        description,
        category="Home",
        completed=True
    )

    assert notes_page.is_note_created(title)

@pytest.mark.ui
def test_delete_note(driver):

    login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"Delete Note {unique_id}"

    notes_page.create_note(
        title,
        "Note created for delete validation",
        category="Home"
    )

    assert notes_page.is_note_created(title)

    assert notes_page.delete_note_by_title(title)

    assert notes_page.is_note_absent(title)


@pytest.mark.ui
def test_edit_note(driver):

    login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"Edit Note {unique_id}"

    updated_title = f"Edited Note {unique_id}"

    updated_description = "Updated by Selenium automation"

    notes_page.create_note(
        title,
        "Original note description",
        category="Home"
    )

    notes_page.edit_note_by_title(
        title,
        updated_title,
        updated_description,
        category="Work",
        completed=True
    )

    assert notes_page.is_note_created(updated_title)

    assert not notes_page.is_note_created(title)

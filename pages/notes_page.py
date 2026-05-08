from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

from utils.logger import get_logger


logger = get_logger()


class NotesPage(BasePage):

    # =========================
    # LOCATORS
    # =========================

    ADD_NOTE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='add-new-note']"
    )

    TITLE_INPUT = (
        By.ID,
        "title"
    )

    DESCRIPTION_INPUT = (
        By.ID,
        "description"
    )
    CATEGORY_DROPDOWN = (
        By.CSS_SELECTOR,
        "[data-testid='note-category']"
    )

    COMPLETED_CHECKBOX = (
        By.CSS_SELECTOR,
        "input[type='checkbox']"
    )

    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='note-submit']"
    )

    NOTES_CONTAINER = (
        By.CSS_SELECTOR,
        "[data-testid='note-card']"
    )

    DELETE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='note-delete']"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-testid='alert-message']"
    )
    CONFIRM_DELETE = (
        By.CSS_SELECTOR,
        "[data-testid='note-delete-confirm']"
    )
    

    # =========================
    # METHODS
    # =========================

    def click_add_note(self):

        logger.info("Clicking add note button")

        self.safe_click(self.ADD_NOTE_BUTTON)

    def is_note_created(self, title):

        logger.info(f"Checking if note created: {title}")

        try:

            note_elements = self.wait.until(
                EC.presence_of_all_elements_located(
                    self.NOTES_CONTAINER
                )
            )

            for note in note_elements:

                note_text = note.text.lower()

                if title.lower() in note_text:

                    logger.info(f"Note found: {title}")

                    return True

            logger.warning(f"Note not found: {title}")

            return False

        except Exception as e:

            logger.error(
                f"Error checking note creation: {e}"
            )

            return False

    def get_notes_count(self):

        logger.info("Getting notes count")

        try:

            # Wait for notes container to be visible
            self.wait.until(
                EC.presence_of_all_elements_located(
                    self.NOTES_CONTAINER
                )
            )

            # Get only direct children (not nested)
            notes = self.driver.execute_script(
                "return document.querySelectorAll('[data-testid=\"note-card\"]').length"
            )

            logger.info(f"Total notes found: {notes}")

            return notes

        except Exception as e:

            logger.error(f"Error getting notes count: {e}")

            return 0

    def delete_first_note(self):

        logger.info("Deleting first note")

        try:

            delete_buttons = self.wait.until(
                EC.presence_of_all_elements_located(
                    self.DELETE_BUTTON
                )
            )

            if delete_buttons:

                # Click first delete button
                self.safe_click(self.DELETE_BUTTON)

                # Confirm deletion
                self.wait.until(
                    EC.element_to_be_clickable(
                        self.CONFIRM_DELETE
                    )
                ).click()

                logger.info("Note deleted successfully")

                # Wait for deletion to complete
                self.wait.until(
                    EC.invisibility_of_element_located(
                        self.CONFIRM_DELETE
                    )
                )

            else:

                logger.warning("No notes to delete")

        except Exception as e:

            logger.error(f"Error deleting note: {e}")

            raise

    def create_note(
        self,
        title,
        description,
        category="Home",
        completed=False
    ):

        logger.info(f"Creating note: {title}")

        self.click_add_note()

        # select category
        dropdown = Select(
            self.wait.until(
                EC.visibility_of_element_located(
                    self.CATEGORY_DROPDOWN
                )
            )
        )

        dropdown.select_by_visible_text(category)

        # completed checkbox
        if completed:

            checkbox = self.wait.until(
                EC.element_to_be_clickable(
                    self.COMPLETED_CHECKBOX
                )
            )

            if not checkbox.is_selected():

                checkbox.click()

        self.send_keys(self.TITLE_INPUT, title)

        self.send_keys(
            self.DESCRIPTION_INPUT,
            description
        )

        # safer click for parallel/grid
        self.safe_click(self.SAVE_BUTTON)

        try:

            # wait until modal/form disappears
            self.wait.until(
                EC.invisibility_of_element_located(
                    self.SAVE_BUTTON
                )
            )

        except Exception as e:

            logger.warning(
                f"Form did not disappear as expected: {e}"
            )

        try:

            # wait until page stabilizes
            self.wait.until(
                EC.element_to_be_clickable(
                    self.ADD_NOTE_BUTTON
                )
            )

        except Exception as e:

            logger.warning(
                f"Page did not stabilize: {e}"
            )
        
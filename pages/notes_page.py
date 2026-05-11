from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
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
        ".modal.show input[type='checkbox']"
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

    EDIT_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='note-edit']"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-testid='alert-message']"
    )
    CONFIRM_DELETE = (
        By.CSS_SELECTOR,
        "[data-testid='note-delete-confirm']"
    )

    @staticmethod
    def _xpath_literal(text):

        if "'" not in text:

            return f"'{text}'"

        if '"' not in text:

            return f'"{text}"'

        parts = text.split("'")

        return "concat(" + ', "\'", '.join(
            f"'{part}'" for part in parts
        ) + ")"

    @classmethod
    def _note_card_by_title_locator(cls, title):

        title_literal = cls._xpath_literal(
            title.lower()
        )

        return (
            By.XPATH,
            "//*[@data-testid='note-card' and "
            "contains("
            "translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz'), "
            f"{title_literal})]"
        )
    

    # =========================
    # METHODS
    # =========================

    def click_add_note(self):

        logger.info("Clicking add note button")

        self.wait.until(
            EC.visibility_of_element_located(
                self.ADD_NOTE_BUTTON
            )
        )

        self.wait.until(
            EC.element_to_be_clickable(
                self.ADD_NOTE_BUTTON
            )
        )

        self.safe_click(
            self.ADD_NOTE_BUTTON
        )

    def is_note_created(self, title):

        logger.info(f"Checking if note created: {title}")

        locator = self._note_card_by_title_locator(title)

        try:

            self.wait.until(
                lambda driver:
                len(driver.find_elements(*locator)) > 0
            )

            logger.info(f"Note found: {title}")

            return True

        except Exception as e:

            logger.error(
                f"Error checking note creation: {e}"
            )

            return False

    def is_note_absent(self, title):

        logger.info(f"Checking if note absent: {title}")

        locator = self._note_card_by_title_locator(title)

        try:

            self.wait.until(
                lambda driver:
                len(driver.find_elements(*locator)) == 0
            )

            return True

        except Exception as e:

            logger.error(
                f"Error checking note absence: {e}"
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

            before_count = self.get_notes_count()

            if before_count == 0:

                logger.warning("No notes to delete")

                return False

            delete_buttons = self.wait.until(
                EC.presence_of_all_elements_located(
                    self.DELETE_BUTTON
                )
            )

            if not delete_buttons:

                logger.warning("No notes to delete")

                return False

            delete_buttons[0].click()

            self.wait.until(
                EC.element_to_be_clickable(
                    self.CONFIRM_DELETE
                )
            ).click()

            self.wait.until(
                lambda driver:
                self.get_notes_count() < before_count
            )

            logger.info("Note deleted successfully")

            return True

        except Exception as e:

            logger.error(f"Error deleting note: {e}")

            raise

    def delete_note_by_title(self, title):

        logger.info(f"Deleting note by title: {title}")

        before_count = self.get_notes_count()

        if before_count == 0:

            logger.warning("No notes to delete")

            return False

        for attempt in range(3):

            try:

                note_card = self.get_note_card_by_title(
                    title
                )

                delete_button = note_card.find_element(
                    *self.DELETE_BUTTON
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView("
                    "{block: 'center'});",
                    delete_button
                )

                try:

                    delete_button.click()

                except Exception:

                    logger.warning(
                        "Normal delete click failed. "
                        "Trying JS click."
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        delete_button
                    )

                try:

                    delete_button.click()

                except Exception:

                    logger.warning(
                        "Delete click intercepted. "
                        "Using JS click."
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        delete_button
                    )

                confirm_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.CONFIRM_DELETE
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    confirm_button
                )

                self.wait.until(
                    lambda driver:
                    len(
                        driver.find_elements(
                            *self._note_card_by_title_locator(
                                title
                            )
                        )
                    ) == 0
                )

                logger.info(
                    f"Note deleted successfully: {title}"
                )

                return True

            except StaleElementReferenceException:

                logger.warning(
                    f"Retry {attempt+1} for stale note card "
                    f"during delete"
                )

                if attempt == 2:

                    raise

        raise TimeoutException(
            f"Note not found for deletion: {title}"
        )

    def get_note_card_by_title(self, title):

        logger.info(f"Finding note card by title: {title}")

        locator = self._note_card_by_title_locator(title)

        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"Note card not found: {title}"
        )

    def get_note_details_by_title(self, title):

        note_card = self.get_note_card_by_title(title)

        return {
            "title": title,
            "text": note_card.text
        }

    def edit_note_by_title(
        self,
        current_title,
        new_title,
        new_description,
        category="Work",
        completed=False
    ):

        logger.info(
            f"Editing note from '{current_title}' "
            f"to '{new_title}'"
        )

        for attempt in range(3):

            try:

                logger.info(
                    f"Waiting for note card visibility: "
                    f"{current_title}"
                )

                locator = self._note_card_by_title_locator(
                    current_title
                )

                self.wait.until(
                    EC.presence_of_element_located(locator)
                )

                self.wait.until(
                    EC.visibility_of_element_located(locator)
                )

                note_card = self.get_note_card_by_title(
                    current_title
                )

                edit_button = note_card.find_element(
                    *self.EDIT_BUTTON
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView("
                    "{block: 'center'});",
                    edit_button
                )

                try:

                    edit_button.click()

                except Exception:

                    logger.warning(
                        "Normal edit click failed. "
                        "Trying JS click."
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        edit_button
                    )

                break

            except StaleElementReferenceException:

                logger.warning(
                    f"Retry {attempt+1} for stale note card "
                    f"during edit"
                )

                if attempt == 2:

                    raise

        dropdown = Select(
            self.wait.until(
                EC.visibility_of_element_located(
                    self.CATEGORY_DROPDOWN
                )
            )
        )

        dropdown.select_by_visible_text(category)

        checkbox = self.wait.until(
            EC.presence_of_element_located(
                self.COMPLETED_CHECKBOX
            )
        )

        if checkbox.is_selected() != completed:

            self.driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

        self.send_keys(self.TITLE_INPUT, new_title)

        self.send_keys(
            self.DESCRIPTION_INPUT,
            new_description
        )

        self.safe_click(self.SAVE_BUTTON)

        self.wait.until(
            lambda driver:
            new_title.lower()
            in driver.page_source.lower()
        )

        logger.info(f"Note edited successfully: {new_title}")

        return True

    def create_note(
        self,
        title,
        description,
        category="Home",
        completed=False
    ):

        logger.info(f"Creating note: {title}")

        self.click_add_note()

        dropdown = Select(
            self.wait.until(
                EC.visibility_of_element_located(
                    self.CATEGORY_DROPDOWN
                )
            )
        )

        dropdown.select_by_visible_text(category)

        if completed:

            checkbox = self.wait.until(
                EC.element_to_be_clickable(
                    self.COMPLETED_CHECKBOX
                )
            )

            if not checkbox.is_selected():

                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox
                )

        self.send_keys(self.TITLE_INPUT, title)

        self.send_keys(
            self.DESCRIPTION_INPUT,
            description
        )

        self.safe_click(self.SAVE_BUTTON)

        try:

            logger.info(
                "Waiting for note modal to close"
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.SAVE_BUTTON
                )
            )

        except Exception as e:

            logger.warning(
                f"Modal did not close properly: {e}"
            )

        import time
        time.sleep(2)

        locator = self._note_card_by_title_locator(
            title
        )

        self.wait.until(
            EC.visibility_of_element_located(
                locator
            )
        )
        time.sleep(2)

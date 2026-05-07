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

        # wait until modal/form disappears
        self.wait.until(
            EC.invisibility_of_element_located(
                self.SAVE_BUTTON
            )
        )

        # wait until page stabilizes
        self.wait.until(
            EC.element_to_be_clickable(
                self.ADD_NOTE_BUTTON
            )
        )
        
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

from utils.logger import get_logger


logger = get_logger()


class LoginPage(BasePage):

    
    # LOCATORS
  

    OPEN_LOGIN = (
        By.XPATH,
        "//a[text()='Login']"
    )

    EMAIL = (
        By.CSS_SELECTOR,
        "input[data-testid='login-email']"
    )

    PASSWORD = (
        By.CSS_SELECTOR,
        "input[data-testid='login-password']"
    )

    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='login-submit']"
    )
    LOGIN_BUTTON_FALLBACK = (
        By.XPATH,
        "//button[@type='submit']"
    )

    ADD_NOTE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='add-new-note']"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-testid='alert-message']"
    )
    LOGOUT_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='logout']"
    )
    LOGOUT_BUTTON_FALLBACK = (
        By.XPATH,
        "//button[contains(text(),'Logout')]"
    )

    
    # METHODS
  

    def login(self, email, password):

        logger.info("Performing login")

        

        self.safe_send_keys(self.EMAIL, email)

        self.safe_send_keys(self.PASSWORD, password)

        self.safe_click(
            self.LOGIN_BUTTON,
            self.LOGIN_BUTTON_FALLBACK
        )

    def is_login_successful(self):

        logger.info("Checking login success")

        return self.is_visible(
            self.ADD_NOTE_BUTTON
        )

    def get_error_message(self):

        logger.info("Waiting for error message")

        element = self.wait.until(
            EC.visibility_of_element_located(
                self.ERROR_MESSAGE
            )
        )

        return element.text
    def logout(self):

        logger.info("Logging out")

        self.safe_click(
            self.LOGOUT_BUTTON,
            self.LOGOUT_BUTTON_FALLBACK
        )


    def is_logged_out(self):

        logger.info(
            "Checking logout success"
        )

        login_button = (
            By.CSS_SELECTOR,
            "[data-testid='open-login-view']"
        )

        return self.is_visible(login_button)
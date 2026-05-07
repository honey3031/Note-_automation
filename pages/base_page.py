from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from config.environment import config

from utils.logger import get_logger

from selenium.common.exceptions import (
    StaleElementReferenceException
)
from selenium.common.exceptions import (
    ElementClickInterceptedException
)
logger = get_logger()


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            config.timeout,
            poll_frequency=0.5
        )
    def open_url(self, url):

        logger.info(f"Opening URL: {url}")

        self.driver.get(url)

    def click(self, locator, retries=3):

        for attempt in range(retries):

            try:

                logger.info(
                    f"Clicking element: {locator}"
                )

                element = self.wait.until(
                    EC.element_to_be_clickable(
                        locator
                    )
                )

                element.click()

                return

            except (
                StaleElementReferenceException,
                ElementClickInterceptedException
            ):

                logger.warning(
                    f"Retry {attempt+1} "
                    f"for click on {locator}"
                )

                if attempt == retries - 1:

                    raise

    def send_keys(self, locator, text):

        logger.info(f"Entering text: {text}")

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        element.clear()

        element.send_keys(text)

    def get_text(self, locator):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        return element.text

    def is_visible(self, locator):

        try:

            self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            return True

        except Exception:
            return False
    def wait_for_visibility(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )


    def wait_for_clickable(self, locator):

        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )
    def js_click(self, locator):

        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )
    def close_google_vignette_popup(self):

        try:

            close_button = self.driver.find_element(
                "xpath",
                "//div[text()='Close']"
            )

            close_button.click()

            logger.info("Popup closed successfully")

        except Exception:

            logger.info("No popup displayed")
    def safe_click(self, locator):

        try:

            self.click(locator)

        except Exception:

            logger.warning(
                f"Normal click failed for {locator}"
            )

            logger.info(
                "Scrolling element into view"
            )

            element = self.wait.until(
                EC.presence_of_element_located(
                    locator
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView("
                "{block: 'center'});",
                element
            )

            logger.info("Trying JS click")

            self.driver.execute_script(
                "arguments[0].click();",
                element
            )
    def safe_send_keys(
        self,
        locator,
        text,
        retries=3
    ):

        for attempt in range(retries):

            try:

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        locator
                    )
                )

                element.clear()

                element.send_keys(text)

                return

            except Exception as e:

                logger.warning(
                    f"Retry {attempt+1} for send_keys"
                )

                if attempt == retries - 1:

                    raise e
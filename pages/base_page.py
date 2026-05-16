from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from config.environment import config

from utils.logger import get_logger

from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException
)
logger = get_logger()
from mcp.failure_analyzer import (
    AIFailureAnalyzer
)

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
                    EC.presence_of_element_located(
                        locator
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView("
                    "{block: 'center'});",
                    element
                )

                self.wait.until(
                    EC.element_to_be_clickable(
                        locator
                    )
                )

                try:

                    element.click()

                except ElementClickInterceptedException:

                    logger.warning(
                        "Normal click intercepted. "
                        "Trying JS click."
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        element
                    )

                return

            except (
                StaleElementReferenceException,
                ElementClickInterceptedException,
                TimeoutException
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
    def wait_for_invisibility(self, locator):

        return self.wait.until(
            EC.invisibility_of_element_located(
                locator
            )
        )
    def js_click(self, locator):

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
    def safe_click(
        self,
        locator,
        fallback_locator=None
    ):

        try:

            logger.info(
                f"Trying primary locator: {locator}"
            )

            self.click(locator)

        except Exception as primary_error:

            logger.warning(
                f"Primary locator failed: "
                f"{primary_error}"
            )

            # AI-assisted failure analysis
            try:

                suggestion = (
                    AIFailureAnalyzer.analyze(
                        str(primary_error)
                    )
                )

                logger.error(
                    f"AI Suggestion: "
                    f"{suggestion}"
                )

            except Exception as ai_error:

                logger.warning(
                    f"AI analysis failed: "
                    f"{ai_error}"
                )

            if fallback_locator:

                logger.info(
                    f"Trying fallback locator: "
                    f"{fallback_locator}"
                )

                self.click(fallback_locator)

            else:

                raise
    def safe_send_keys(
        self,
        locator,
        text,
        fallback_locator=None,
        retries=3
    ):

        for attempt in range(retries):

            try:

                logger.info(
                    f"Trying send_keys "
                    f"with locator: {locator}"
                )

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        locator
                    )
                )

                element.clear()

                element.send_keys(text)

                return

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as e:

                logger.warning(
                    f"Retry {attempt+1} "
                    f"for send_keys"
                )

                # AI-assisted failure analysis
                try:

                    suggestion = (
                        AIFailureAnalyzer.analyze(
                            str(e)
                        )
                    )

                    print(
                        f"\nAI Suggestion:\n"
                        f"{suggestion}\n"
                    )

                except Exception as ai_error:

                    logger.warning(
                        f"AI analysis failed: "
                        f"{ai_error}"
                    )

                if (
                    fallback_locator
                    and attempt == retries - 1
                ):

                    logger.info(
                        f"Trying fallback locator: "
                        f"{fallback_locator}"
                    )

                    fallback_element = self.wait.until(
                        EC.visibility_of_element_located(
                            fallback_locator
                        )
                    )

                    fallback_element.clear()

                    fallback_element.send_keys(text)

                    return

                if attempt == retries - 1:

                    raise e

                
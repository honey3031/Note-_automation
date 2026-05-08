from selenium.webdriver.common.by import By


class LocatorIntelligence:

    @staticmethod
    def candidates(test_id, tag="*"):

        return [
            (By.CSS_SELECTOR, f"[data-testid='{test_id}']"),
            (By.CSS_SELECTOR, f"{tag}[data-testid='{test_id}']"),
            (By.XPATH, f"//*[@data-testid='{test_id}']")
        ]

    @staticmethod
    def first_available(driver, candidates):

        for locator in candidates:

            if driver.find_elements(*locator):

                return locator

        return None

    @staticmethod
    def locator_suggestion(test_id):

        return {
            "preferred": f"[data-testid='{test_id}']",
            "fallbacks": [
                f"//*[@data-testid='{test_id}']",
                f"//*[contains(@data-testid, '{test_id}')]"
            ],
            "reason": (
                "Stable data-testid attributes are less brittle "
                "than style or layout based selectors."
            )
        }

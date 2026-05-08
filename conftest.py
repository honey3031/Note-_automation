import pytest
import os

from fixtures.browser_fixture import get_driver

from utils.helpers import take_screenshot
from config.environment import config


def pytest_sessionstart(session):

    os.makedirs("allure-results", exist_ok=True)

    try:

        with open(
            "allure-results/environment.properties",
            "w",
            encoding="utf-8"
        ) as env_file:

            env_file.write(
                "\n".join(
                    [
                        "Application=ExpandTesting Notes",
                        f"Base_URL={config.base_url}",
                        f"API_URL={config.api_url}",
                        f"Execution={config.execution}",
                        f"Browser={config.browser}"
                    ]
                )
            )

    except PermissionError:

        pass


@pytest.fixture(scope="function")
def driver():

    driver = get_driver()

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)

def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            screenshot_path = take_screenshot(
                driver,
                item.name
            )

            try:

                import allure

                allure.attach.file(
                    screenshot_path,
                    name=item.name,
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception:

                pass

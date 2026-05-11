import os
from pathlib import Path
from datetime import datetime, UTC

import pytest
import allure

from fixtures.browser_fixture import get_driver
from utils.helpers import take_screenshot
from utils.logger import get_logger
from config.environment import config


logger = get_logger()


def pytest_sessionstart(session):

    allure_dir = Path("allure-results")

    allure_dir.mkdir(
        exist_ok=True
    )

    env_file_path = (
        allure_dir / "environment.properties"
    )

    try:

        with open(
            env_file_path,
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
                        f"Browser={config.browser}",
                        f"Environment={config.environment}"
                    ]
                )
            )

        logger.info(
            "Allure environment file created"
        )

    except Exception as e:

        logger.warning(
            f"Failed to create "
            f"environment.properties: {e}"
        )


@pytest.fixture(scope="function")
def driver():

    driver = get_driver()

    yield driver

    try:

        driver.quit()

        logger.info(
            "Browser closed successfully"
        )

    except Exception as e:

        logger.warning(
            f"Driver quit failed: {e}"
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if (
        report.when == "call"
        and report.failed
    ):

        driver = item.funcargs.get("driver")

        if driver:

            timestamp = (
                datetime.now(UTC)
                .strftime("%Y%m%d_%H%M%S")
            )

            screenshot_name = (
                f"{item.name}_{timestamp}"
            )

            screenshot_path = take_screenshot(
                driver,
                screenshot_name
            )

            try:

                allure.attach.file(
                    screenshot_path,
                    name=screenshot_name,
                    attachment_type=
                    allure.attachment_type.PNG
                )

                logger.info(
                    "Failure screenshot attached "
                    "to Allure report"
                )

            except Exception as e:

                logger.warning(
                    f"Allure attachment failed: {e}"
                )
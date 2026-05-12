import os
from pathlib import Path
from datetime import datetime, UTC

import pytest
import allure

from fixtures.browser_fixture import get_driver
from utils.helpers import take_screenshot
from utils.logger import get_logger
from utils.ai_suggestions import AISuggestions
from config.environment import config


logger = get_logger()

def generate_failure_analysis(
    test_name,
    error_message
):

    probable_reason = (
        "Unknown issue"
    )

    suggested_fix = (
        "Check logs and screenshots"
    )

    error_lower = error_message.lower()

    if "timeout" in error_lower:

        probable_reason = (
            "Element synchronization issue"
        )

        suggested_fix = (
            "Increase explicit waits "
            "or improve locator stability"
        )

    elif "no such element" in error_lower:

        probable_reason = (
            "Locator not found"
        )

        suggested_fix = (
            "Verify locator strategy "
            "or page structure"
        )

    elif "stale element" in error_lower:

        probable_reason = (
            "DOM updated before interaction"
        )

        suggested_fix = (
            "Retry interaction after "
            "element refresh"
        )

    elif "connection refused" in error_lower:

        probable_reason = (
            "Selenium Grid unavailable"
        )

        suggested_fix = (
            "Verify Docker containers "
            "and Grid startup"
        )

    ai_suggestion = (
        AISuggestions.analyze_failure(
            error_message
        )
    )

    report = (
        f"TEST: {test_name}\n\n"
        f"ERROR:\n{error_message}\n\n"
        f"PROBABLE REASON:\n"
        f"{probable_reason}\n\n"
        f"SUGGESTED FIX:\n"
        f"{suggested_fix}\n\n"
        f"AI-INSPIRED SUGGESTION:\n"
        f"{ai_suggestion}\n"
    )

    os.makedirs(
        "failure-analysis",
        exist_ok=True
    )

    file_path = (
        f"failure-analysis/"
        f"{test_name}.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

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
            generate_failure_analysis(
                item.name,
                str(call.excinfo.value)
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
            
            
import pytest

from fixtures.browser_fixture import get_driver

from utils.helpers import take_screenshot


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

            take_screenshot(
                driver,
                item.name
            )
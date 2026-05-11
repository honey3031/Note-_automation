from pathlib import Path
from datetime import datetime, UTC

from utils.logger import get_logger


logger = get_logger()


def take_screenshot(driver, name):

    screenshots_dir = Path(
        "screenshots"
    )

    screenshots_dir.mkdir(
        exist_ok=True
    )

    timestamp = (
        datetime.now(UTC)
        .strftime("%Y%m%d_%H%M%S_%f")
    )

    screenshot_path = (
        screenshots_dir /
        f"{name}_{timestamp}.png"
    )

    try:

        driver.save_screenshot(
            str(screenshot_path)
        )

        logger.info(
            f"Screenshot saved: "
            f"{screenshot_path}"
        )

    except Exception as e:

        logger.warning(
            f"Failed to save screenshot: {e}"
        )

    return str(screenshot_path)
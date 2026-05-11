import logging
from pathlib import Path
from datetime import datetime, UTC


def get_logger(name="framework"):

    logs_dir = Path("logs")

    logs_dir.mkdir(
        exist_ok=True
    )

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if logger.handlers:

        return logger

    formatter = logging.Formatter(
        (
            "%(asctime)s "
            "[%(levelname)s] "
            "%(name)s - %(message)s"
        )
    )

    # console logging
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    # unique log file
    timestamp = (
        datetime.now(UTC)
        .strftime("%Y%m%d_%H%M%S")
    )

    log_file = (
        logs_dir /
        f"test_execution_{timestamp}.log"
    )

    try:

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        file_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            file_handler
        )

    except Exception as e:

        logger.warning(
            f"Failed to initialize "
            f"file logging: {e}"
        )

    logger.propagate = False

    return logger
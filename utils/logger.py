import logging
from pathlib import Path


LOG_FILE = "logs/framework.log"


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

    try:

        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )

        file_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            file_handler
        )

    except Exception:
        pass

    logger.propagate = False

    return logger
import logging
import os


def get_logger():

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        try:

            file_handler = logging.FileHandler(
                "logs/test_execution.log",
                encoding="utf-8"
            )

            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        except PermissionError:

            logger.warning(
                "Log file is locked; continuing with console logging"
            )

    return logger

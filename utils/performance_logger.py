import csv
import os
from datetime import datetime, UTC
from utils.logger import get_logger


logger = get_logger()


class PerformanceLogger:

    REPORT_PATH = os.path.join(
        "performance_logs",
        "performance_trends.csv"
    )

    @classmethod
    def record(
        cls,
        test_name,
        metric,
        value_seconds,
        status="pass"
    ):

        os.makedirs(
            "performance_logs",
            exist_ok=True
        )

        file_exists = os.path.exists(cls.REPORT_PATH)

        with open(
            cls.REPORT_PATH,
            "a",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.writer(csv_file)

            if not file_exists:

                writer.writerow(
                    [
                        "timestamp",
                        "test_name",
                        "metric",
                        "value_seconds",
                        "status"
                    ]
                )

            writer.writerow(
                [
                    datetime.now(UTC).isoformat(),
                    test_name,
                    metric,
                    f"{value_seconds:.3f}",
                    status
                ]
            )

        logger.info(
            f"Performance metric recorded: "
            f"{metric}={value_seconds:.3f}s"
        )

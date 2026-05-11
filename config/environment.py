import os
from pathlib import Path

import yaml


class Config:

    def __init__(self):

        config_path = (
            Path(__file__)
            .resolve()
            .parent / "config.yaml"
        )

        if not config_path.exists():

            raise FileNotFoundError(
                f"Config file not found: "
                f"{config_path}"
            )

        with open(config_path, "r") as file:

            data = yaml.safe_load(file)

        self.environment = os.getenv(
            "ENVIRONMENT",
            data.get("environment", "qa")
        )

        self.base_url = os.getenv(
            "BASE_URL",
            data["base_url"]
        )

        self.api_url = os.getenv(
            "API_URL",
            data["api_url"]
        )

        self.browser = os.getenv(
            "BROWSER",
            data["browser"]
        )

        self.execution = os.getenv(
            "EXECUTION",
            data["execution"]
        )

        self.grid_url = os.getenv(
            "GRID_URL",
            data.get(
                "grid_url",
                "http://localhost:4444/wd/hub"
            )
        )

        self.timeout = int(
            os.getenv(
                "TIMEOUT",
                data.get("timeout", 20)
            )
        )

        self.headless = (
            str(
                os.getenv(
                    "HEADLESS",
                    data.get("headless", False)
                )
            ).lower() == "true"
        )

        self.parallel_workers = int(
            os.getenv(
                "PARALLEL_WORKERS",
                data.get(
                    "parallel_workers",
                    3
                )
            )
        )


config = Config()
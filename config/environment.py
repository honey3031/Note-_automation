import os

import yaml


class Config:

    def __init__(self):
        with open("config/config.yaml", "r") as file:
            data = yaml.safe_load(file)

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
        self.timeout = data["timeout"]


config = Config()

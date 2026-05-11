import requests

from utils.logger import get_logger


logger = get_logger(__name__)


class BaseAPI:

    def __init__(self, base_url, headers=None):

        self.base_url = base_url

        self.session = requests.Session()

        self.session.headers.update(
            headers or {}
        )

    def get(self, endpoint, timeout=10):

        logger.info(
            f"GET Request: {endpoint}"
        )

        return self.session.get(
            f"{self.base_url}{endpoint}",
            timeout=timeout
        )

    def post(
        self,
        endpoint,
        payload,
        timeout=10
    ):

        logger.info(
            f"POST Request: {endpoint}"
        )

        return self.session.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            timeout=timeout
        )

    def put(
        self,
        endpoint,
        payload,
        timeout=10
    ):

        logger.info(
            f"PUT Request: {endpoint}"
        )

        return self.session.put(
            f"{self.base_url}{endpoint}",
            json=payload,
            timeout=timeout
        )

    def delete(
        self,
        endpoint,
        timeout=10
    ):

        logger.info(
            f"DELETE Request: {endpoint}"
        )

        return self.session.delete(
            f"{self.base_url}{endpoint}",
            timeout=timeout
        )
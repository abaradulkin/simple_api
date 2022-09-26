import logging
import requests
import json


log = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url):
        self._base_url = base_url
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.session = requests.Session()

    def __send(self, method, endpoint, payload=None, **kwargs):
        log.debug(method, endpoint, payload, kwargs)
        response = method(f"{self._base_url}{endpoint}", data=json.dumps(payload), headers=self.headers,  **kwargs)
        log.debug(response.status_code, response.json())
        return response

    def get(self, endpoint, **kwargs):
        return self.__send(requests.get, endpoint)

    def post(self, endpoint, payload, **kwargs):
        return self.__send(requests.post, endpoint, payload=payload, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.__send(requests.delete, endpoint, **kwargs)

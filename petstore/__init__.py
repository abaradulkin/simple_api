import requests
import json


class APIClient:
    def __init__(self, base_url):
        self._base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint):
        print("GET", f"{self._base_url}{endpoint}")
        response = self.session.get(f"{self._base_url}{endpoint}")
        print(response.json())
        return response

    def post(self, endpoint, body, headers=None):
        headers = headers if headers else {"Content-Type": "application/json"}
        print("POST", f"{self._base_url}{endpoint}", json.dumps(body), headers)
        response = self.session.post(f"{self._base_url}{endpoint}", data=json.dumps(body), headers=headers)
        print(response.json())
        return response

    def delete(self, endpoint, headers=None):
        print("DELETE", f"{self._base_url}{endpoint}", headers)
        response = self.session.post(f"{self._base_url}{endpoint}", headers=headers)
        print(response.text)
        return response


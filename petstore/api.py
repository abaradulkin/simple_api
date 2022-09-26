import logging

from . import APIClient


log = logging.getLogger(__name__)


class PetStoreApi(APIClient):
    def get_pet(self, pet_id, **kwargs):
        log.info(f"Get pet information for pet with ID: {pet_id}")
        response = self.get(f"/pet/{pet_id}")
        return response

    def create_pet(self, payload, **kwargs):
        log.info(f"Create pet with parameters: {payload}")
        response = self.post("/pet", payload=payload)
        return response

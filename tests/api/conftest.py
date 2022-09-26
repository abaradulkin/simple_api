import pytest
from faker import Faker

from petstore.api import PetStoreApi


@pytest.fixture(scope="session")
def petstore_api():
    client = PetStoreApi("https://petstore.swagger.io/v2")
    yield client


@pytest.fixture(scope="session")
def fake():
    yield Faker()

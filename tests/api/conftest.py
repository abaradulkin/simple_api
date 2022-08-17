import pytest
from faker import Faker

from petstore import APIClient


@pytest.fixture(scope="session")
def petstore_api():
    client = APIClient("https://petstore.swagger.io/v2")
    yield client


@pytest.fixture(scope="session")
def fake():
    yield Faker()

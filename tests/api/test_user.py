import pytest
from faker import Faker

from petstore.assertions import assert_success_response
from petstore.objects import create_pet


class TestSmokeUserCreation:
    @pytest.fixture
    def user(self, petstore_api):
        fake = Faker()
        print(dir(fake))
        user_data = {"username": fake.user_name(), "password": fake.password()}
        petstore_api.post("/user", body=user_data)
        yield user_data
        petstore_api.delete(f"/user/{user_data['username']}")

    def test_create_user(self, petstore_api, user):
        response = petstore_api.get(f"/user/{user['username']}")


    def test_login(self, petstore_api, user):
        petstore_api.get(f"/user/login?username={user['username']}&password={user['password']}")


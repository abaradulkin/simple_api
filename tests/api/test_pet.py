import pytest
import schemathesis

from petstore.assertions import assert_success_response
from petstore.objects import create_pet


schema = schemathesis.from_uri("https://petstore.swagger.io/v2/swagger.json")


class TestAddPetToPetStore:
    def test_add_pet(self, petstore_api):
        body = create_pet()
        response = petstore_api.post("/pet", body=body)
        assert_success_response(response, body)
        response = petstore_api.get(f"/pet/{response.json()['id']}")
        assert_success_response(response, body)

    def test_add_pet_without_photo_url(self, petstore_api, fake):
        name = fake.first_name()
        pet_id = fake.random_int()
        status = "availiable"
        body = {
            "id": pet_id,
            "name": name,
            "status": status

        }
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()["id"] == pet_id
        assert response.json()["name"] == name
        assert response.json()["status"] == status
        assert not response.json()["photoUrls"]

    def test_add_pet_without_id(self, petstore_api, fake):
        name = fake.first_name()
        image_url = fake.image_url()
        status = "availiable"
        body = {
            "name": name,
            "photoUrls": [image_url],
            "status": status

        }
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)
        assert response.json()["id"] > 0
        assert image_url in response.json()["photoUrls"]
        assert response.json()["name"] == name
        assert response.json()["status"] == status

    def test_add_pet_without_status(self, petstore_api, fake):
        name = fake.first_name()
        image_url = fake.image_url()
        pet_id = fake.random_int()
        body = {
            "id": pet_id,
            "name": name,
            "photoUrls": [image_url]
        }
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()["id"] == pet_id
        assert image_url in response.json()["photoUrls"]
        assert response.json()["name"] == name
        assert "status" not in response.json()

    def test_add_pet_without_name(self, petstore_api, fake):
        name = fake.first_name()
        image_url = fake.image_url()
        pet_id = fake.random_int()
        status = "availiable"
        body = {
            "id": pet_id,
            "photoUrls": [image_url],
            "status": status

        }
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()["id"] == pet_id
        assert image_url in response.json()["photoUrls"]
        assert "name" not in response.json()
        assert response.json()["status"] == status

    @pytest.mark.parametrize("param", ["name", "status"])
    def test_add_pet_empty_optional_param(self, petstore_api, param):
        body = create_pet()
        body[param] = ""
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()[param] == ""

    def test_add_pet_empty_id(self, petstore_api):
        body = create_pet()
        body["id"] = ""
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)
        assert response.json()["id"] > 0

    def test_add_pet_extra_param(self, petstore_api):
        body = create_pet()
        body["extra"] = "extra"
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert "extra" not in response.json()

    def test_add_pet_invalid_json(self, petstore_api):
        body = "{'id': 0"
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 500
        assert "something bad happened" not in response.json()["message"]

    @pytest.mark.parametrize("id", ["invalid", -1])
    def test_add_pet_invalid_id(self, petstore_api, id):
        body = create_pet()
        body["id"] = id
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 500
        assert "something bad happened" not in response.json()["message"]

    def test_add_pet_invalid_name(self, petstore_api):
        body = create_pet()
        body["name"] = 0
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()["name"] == "0"

    def test_add_pet_special_char_name(self, petstore_api):
        body = create_pet()
        body["name"] = "test123$%^*"
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()["name"] == body["name"]

    def test_add_pet_invalid_status(self, petstore_api):
        body = create_pet()
        body["status"] = 0
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()["status"] == "0"

    def test_add_pet_unexisting_status(self, petstore_api):
        body = create_pet()
        body["status"] = "unexisting_status"
        response = petstore_api.post("/pet", body=body)
        assert response.status_code == 200
        assert response.json()["status"] == "unexisting_status"

###
def test_get_pet_not_exists(petstore_api):
    """ Check getting pet with unexisting ID """
    response = petstore_api.get(f"/pet/{0}")
    assert response.status_code == 404
    print(response.headers)
    assert response.json()["message"] == "Pet not found"
    assert response.json()["type"] == "error"
    assert response.json()["code"] == 1
    print(schema)
    from pprint import pprint
    pprint(schema["/pet/{petId}"])
    pprint(schema["/pet/{petId}"]["GET"])
    schema["/pet/{petId}"]["GET"].validate_response(response)
    schema["/pet/{petId}"]["GET"].is_response_valid(response)


@pytest.mark.parametrize("invalid_char", ("a", "*"))
def test_get_pet_invalid_id_special_char(invalid_char, petstore_api):
    """ Check getting pet with invalid ID"""
    response = petstore_api.get(f"/pet/{invalid_char}")
    assert response.status_code == 404
    assert response.json()["message"] == f"java.lang.NumberFormatException: For input string: \"{invalid_char}\""
    assert response.json()["type"] == "unknown"
    assert response.json()["code"] == 1

from faker import Faker


def create_pet():
    fake = Faker()
    name = fake.first_name()
    image_url = fake.image_url()
    pet_id = fake.random_int()
    status = "availiable"
    return {
        "id": pet_id,
        "name": name,
        "photoUrls": [image_url],
        "status": status
    }
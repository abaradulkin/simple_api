from faker import Faker

fake = Faker()


PET_SCHEMA = {
  'id': {'type': 'integer'},
  'category': {
    'type': 'dict', 'schema': {'id': {'type': 'integer'}, 'name': {'type': 'string'}}
  },
  'photoUrls': {
      'type': 'list', 'schema': {'type': 'string'}
  },
  'tags': {
    'type': 'list', 'schema': {
        'type': 'dict', 'schema': {'id': {'type': 'integer'}, 'name': {'type': 'string'}}
      }
  },
  'name': {'type': 'string'},
  'status': {'type': 'string'}
}


def create_pet():
    return {
        "id": fake.random_int(),
        "category": {"id": fake.random_int(), "name": fake.word()},
        "tags": [{"id": fake.random_int(), "name": fake.word()}],
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "status": "availiable"
    }
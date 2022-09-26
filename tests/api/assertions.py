from assertpy import assert_that, soft_assertions


def assert_pet_response(response, actual_data):
    with soft_assertions():
        assert_that(response.status_code).is_equal_to(200)
        for key in actual_data.keys():
            assert assert_that(response.json()[key]).is_equal_to(actual_data[key])

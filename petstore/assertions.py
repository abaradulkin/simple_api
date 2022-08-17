

def assert_success_response(response, actual_data):
    assert response.status_code == 200
    for key in actual_data.keys():
        assert response.json()[key] == actual_data[key]

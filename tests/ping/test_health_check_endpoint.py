ENDPOINT = "ping"

def test_check_endpoint(api_client):
    response = api_client.get(ENDPOINT)
    assert response.status_code == 201
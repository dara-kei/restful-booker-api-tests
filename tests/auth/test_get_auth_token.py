from schemas.schema_get_token import auth_token_schema
from jsonschema import validate


ENDPOINT = 'auth'

def test_getting_auth_token_with_valid_data(api_client):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'username' : 'admin',
        'password' : 'password123'
    }

    response = api_client.post(ENDPOINT, json=payload, headers=headers)
    assert response.status_code == 200
    validate(response.json(), auth_token_schema)



def test_trying_to_get_token_with_invalid_password(api_client):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'username' : 'admin',
        'password' : '123'
    }
    response = api_client.post(ENDPOINT, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()['reason'] == 'Bad credentials'


def test_trying_to_get_token_with_invalid_username(api_client):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'username' : 'user',
        'password' : 'password123'
    }
    response = api_client.post(ENDPOINT, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()['reason'] == 'Bad credentials'


def test_trying_to_get_token_with_empty_data(api_client):
    headers = {'Content-Type': 'application/json'}
    payload = {}
    response = api_client.post(ENDPOINT, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()['reason'] == 'Bad credentials'


def test_trying_to_get_token_with_invalid_data(api_client):
    headers = {'Content-Type': 'application/json'}
    payload = "admin"
    response = api_client.post(ENDPOINT, json=payload, headers=headers)
    assert response.status_code == 400
    assert response.text == "Bad Request"

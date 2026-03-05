from schemas.schema_get_token import aut_token_schema
from jsonschema import validate, ValidationError


ENDPOINT = 'auth'

def test_getting_auth_api_with_valid_data(api_client):
    headers = {'Content-Type': 'application/json'}
    data = {
        'username' : 'admin',
        'password' : 'password123'
    }

    response = api_client.post(ENDPOINT, json=data, headers=headers)
    assert response.status_code == 200
    try:
        validate(response.json(), aut_token_schema)
    except ValidationError as e:
        print("Alarm")
        raise e


def test_trying_to_get_token_with_invalid_password(api_client):
    headers = {'Content-Type': 'application/json'}
    data = {
        'username' : 'admin',
        'password' : '123'
    }
    response = api_client.post(ENDPOINT, json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()['reason'] == 'Bad credentials'


def test_trying_to_get_token_with_invalid_username(api_client):
    headers = {'Content-Type': 'application/json'}
    data = {
        'username' : 'user',
        'password' : '123'
    }
    response = api_client.post(ENDPOINT, json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()['reason'] == 'Bad credentials'


def test_trying_to_get_token_with_empty_data(api_client):
    headers = {'Content-Type': 'application/json'}
    data = {}
    response = api_client.post(ENDPOINT, json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()['reason'] == 'Bad credentials'


def test_trying_to_get_token_with_invalid_data(api_client):
    headers = {'Content-Type': 'application/json'}
    data = "admin"
    response = api_client.post(ENDPOINT, json=data, headers=headers)
    assert response.status_code == 400

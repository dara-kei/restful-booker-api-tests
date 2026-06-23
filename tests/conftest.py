import pytest
from utils.api_client import ApiClient
from utils.logger_config import logger



@pytest.fixture(scope="session")
def api_client():
    return ApiClient()


@pytest.fixture(scope="session")
def token(api_client):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    payload = {
        'username' : 'admin',
        'password' : 'password123'
    }
    response = api_client.post('auth', json=payload, headers=headers)

    return response.json()['token']



@pytest.fixture(scope="function")
def create_booking(api_client, token):
    headers = {'Content-Type': 'application/json'}
    data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = api_client.post('booking', json=data, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    response_id = response_json['bookingid']

    logger.info(f"Booking created. id={response_id}")


    yield {'bookingid': response_id,
           'data' : response_json}

    logger.info(f"Deleting booking. id={response_id}")

    delete_response = api_client.delete(f'booking/{response_id}', headers={'Cookie' : f'token={token}'})
    assert delete_response.status_code == 201
    logger.info(
        f"Booking deleted. id={response_id}, status_code={delete_response.status_code}"
    )


@pytest.fixture(scope="function")
def create_booking_for_delete(api_client, token):
    headers = {'Content-Type': 'application/json'}
    data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = api_client.post('booking', json=data, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    response_id = response_json['bookingid']

    logger.info(f"Booking created. id={response_id}")

    yield {'bookingid': response_id,
           'data' : response_json}
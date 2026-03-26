import pytest
import requests
from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    return ApiClient()


@pytest.fixture(scope="session")
def get_token(api_client):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    payload = {
        'username' : 'admin',
        'password' : 'password123'
    }
    response = api_client.post('auth', json=payload, headers=headers)

    return response.json()['token']



@pytest.fixture(scope="function")
def create_booking(api_client, get_token):
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
    booking = api_client.post('booking', json=data, headers=headers)
    assert booking.status_code == 200
    booking_json = booking.json()
    booking_id = booking_json['bookingid']
    yield {'bookingid': booking_id,
           'data' : booking_json}

    api_client.delete(f'booking/{booking_id}', headers={'Cookie' : f'token ={get_token}'})

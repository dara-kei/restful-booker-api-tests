from wsgiref import headers

from schemas.schema_get_one_booking import get_one_booking_schema
from jsonschema import validate
import pytest


ENDPOINT = 'booking'


def test_update_booking(api_client, create_booking, token):
    payload = {
    "firstname" : "James",
    "lastname" : "Brown",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    headers = {'Cookie' : f'token={token}'}
    response = api_client.put(f'{ENDPOINT}/{create_booking['bookingid']}', json=payload, headers=headers)
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_one_booking_schema)
    assert actual_response['firstname'] == 'James'


def test_update_booking_without_last_name(api_client, create_booking, token):
    payload = {
    "firstname" : "James",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    headers = {'Cookie' : f'token={token}'}
    response = api_client.put(f'{ENDPOINT}/{create_booking['bookingid']}', json=payload, headers=headers)
    assert response.status_code == 400


def test_update_booking_without_token(api_client, create_booking):
    payload = {
    "firstname" : "James",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    response = api_client.put(f'{ENDPOINT}/{create_booking['bookingid']}', json=payload)
    assert response.status_code == 403


def test_update_not_existing_booking(api_client, token):
    payload = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    headers = {'Cookie': f'token={token}'}
    response = api_client.put(f'{ENDPOINT}/99999999', json=payload, headers=headers)
    assert response.status_code == 405


@pytest.mark.xfail(
    reason="API-XX: PUT /booking incorrectly processes invalid booking ids"
)
@pytest.mark.parametrize("booking_id", ["1abc", "1.1", "01"])
def test_update_booking_with_invalid_id(api_client, token, booking_id):
    payload = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    headers = {'Cookie': f'token={token}'}
    response = api_client.put(f'{ENDPOINT}/{booking_id}', json=payload, headers=headers)
    assert response.status_code == 404


@pytest.mark.xfail(
    reason="Known bug: API accepts negative total price during booking update"
)
def test_update_booking_with_negative_price(api_client,create_booking, token):
    payload = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": -111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    headers = {'Cookie': f'token={token}'}
    response = api_client.put(f'{ENDPOINT}/{create_booking["bookingid"]}', json=payload, headers=headers)
    assert response.status_code == 400


@pytest.mark.xfail(
    reason="Known bug: API accepts checkout date earlier than checkin date during booking update"
)
def test_update_booking_invalid_date(api_client,create_booking, token):
    payload = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2020-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    headers = {'Cookie': f'token={token}'}
    response = api_client.put(f'{ENDPOINT}/{create_booking["bookingid"]}', json=payload, headers=headers)
    assert response.status_code == 400
    
from schemas.schema_create_booking import create_booking_schema
from jsonschema import validate, ValidationError
import pytest


ENDPOINT = 'booking'


def test_create_booking(api_client):
    data = {
    "firstname" : "Jim",
    "lastname" : "Brown",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    # headers можно не писать, так как json=data автоматически добавляет нужные headers
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    response = api_client.post(ENDPOINT, json = data, headers = headers)
    assert response.status_code == 200
    actual_result = response.json()
    validate(actual_result, create_booking_schema)
    assert actual_result['booking']['firstname'] == 'Jim'
    assert actual_result['booking']['lastname'] == 'Brown'
    assert actual_result['booking']['totalprice'] == 111
    assert isinstance(actual_result['bookingid'], int)
    # проверка, что запись создалась
    response2 = api_client.get(f'{ENDPOINT}/{actual_result["bookingid"]}')
    assert response2.status_code == 200


def test_create_booking_with_invalid_data(api_client):
    data = {
    "lastname" : "Brown",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    response = api_client.post(ENDPOINT, json = data)
    assert response.status_code == 500


def test_create_booking_without_data(api_client):
    data = {}
    response = api_client.post(ENDPOINT, json = data)
    assert response.status_code == 500

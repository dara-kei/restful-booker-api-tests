from schemas.schema_create_booking import create_booking_schema
from jsonschema import validate
import pytest


ENDPOINT = 'booking'


def test_create_booking(api_client):
    payload = {
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
    # headers = {'Content-Type': 'application/json',
    #            'Accept': 'application/json'}
    response = api_client.post(ENDPOINT, json = payload)
    assert response.status_code == 200
    actual_result = response.json()
    validate(actual_result, create_booking_schema)
    assert actual_result['booking'] == payload
    assert isinstance(actual_result['bookingid'], int)
    # проверка, что запись создалась
    response2 = api_client.get(f'{ENDPOINT}/{actual_result["bookingid"]}')
    assert response2.status_code == 200


@pytest.mark.xfail(
    reason="Known bug: POST /booking returns 500 when firstname is missing"
)
def test_create_booking_without_first_name(api_client):
    payload = {
    "lastname" : "Brown",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    response = api_client.post(ENDPOINT, json = payload)
    assert response.status_code == 400


@pytest.mark.xfail(
    reason="Known bug: POST /booking creates booking with negative total price"
)
def test_create_booking_with_negative_price(api_client):
    payload = {
    "firstname" : "Jim",
    "lastname" : "Brown",
    "totalprice" : -111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    response = api_client.post(ENDPOINT, json = payload)
    assert response.status_code == 400


@pytest.mark.xfail(reason="Known bug: checkout date earlier than checkin date is accepted")
def test_create_booking_with_negative_price(api_client):
    payload = {
    "firstname" : "Jim",
    "lastname" : "Brown",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2020-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    response = api_client.post(ENDPOINT, json = payload)
    assert response.status_code == 400


@pytest.mark.xfail(
    reason="Known bug: POST /booking returns 500 when data is missing"
)
def test_create_booking_without_data(api_client):
    payload = {}
    response = api_client.post(ENDPOINT, json = payload)
    assert response.status_code == 400



from schemas.schema_get_one_booking import get_one_booking_schema
from jsonschema import validate


ENDPOINT = 'booking'


def test_partial_update_booking(api_client, create_booking, get_token):
    data = {
    "firstname" : "James",
    "lastname" : "Brown"
}
    headers = {'Cookie' : f'token={get_token}'}
    response = api_client.patch(f'{ENDPOINT}/{create_booking['bookingid']}', json=data, headers=headers)
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_one_booking_schema)
    assert actual_response['firstname'] == 'James'
    assert actual_response['lastname'] == 'Brown'


def test_partial_update_booking_without_data(api_client, create_booking, get_token):
    data = {}
    headers = {'Cookie' : f'token={get_token}'}
    response = api_client.patch(f'{ENDPOINT}/{create_booking['bookingid']}', json=data, headers=headers)
    assert response.status_code == 200


def test_partial_update_booking_without_token(api_client, create_booking):
    data = {
    "firstname" : "James",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}
    response = api_client.patch(f'{ENDPOINT}/{create_booking['bookingid']}', json=data)
    assert response.status_code == 403
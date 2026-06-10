from schemas.schema_get_one_booking import get_one_booking_schema
from jsonschema import validate # надо установить библиотеку pip install jsonschema
import pytest


ENDPOINT = 'booking'


def test_get_booking_by_id(api_client, create_booking):
    response = api_client.get(f'{ENDPOINT}/{create_booking["bookingid"]}')
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_one_booking_schema)
    assert actual_response == create_booking['data']['booking']


@pytest.mark.parametrize("not_existing_id", [0, -1, 999999999],
                         ids=["zero", "negative", "very_large"])
def test_get_booking_with_not_existing_id(api_client, not_existing_id):
    response = api_client.get(f'{ENDPOINT}/{not_existing_id}')
    assert response.status_code == 404


@pytest.mark.xfail(
    reason="API-25: GET /booking incorrectly processes invalid booking id values"
)
@pytest.mark.parametrize("invalid_id", ["1.1", "01", "0001", "%20", "abc", "1abc"])
def test_get_booking_with_invalid_id(api_client, invalid_id):
    response = api_client.get(f'{ENDPOINT}/{invalid_id}')
    assert response.status_code == 404, (
        f"id={invalid_id}\n"
        f"status={response.status_code}\n"
        f"body={response.text}"
    )


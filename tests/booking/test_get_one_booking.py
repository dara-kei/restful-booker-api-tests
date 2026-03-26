from schemas.schema_get_one_booking import get_one_booking_schema
from jsonschema import validate, ValidationError
import pytest

from tests.conftest import api_client


ENDPOINT = 'booking'


def test_get_bookings_id_filter_by_id(api_client, create_booking):
    response = api_client.get(f'{ENDPOINT}/{create_booking['bookingid']}')
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_one_booking_schema)
    assert actual_response == create_booking['data']['booking']


@pytest.mark.parametrize("invalid_id", ['000', 'ghj'])
def test_get_bookings_id_with_invalid_bookingid(api_client,invalid_id):
    response = api_client.get(f'{ENDPOINT}/{invalid_id}')
    assert response.status_code == 404

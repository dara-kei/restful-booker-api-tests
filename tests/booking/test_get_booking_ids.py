from schemas.schema_get_booking_ids import get_bookings_ids_schema
from jsonschema import validate
import pytest

ENDPOINT = 'booking'


def test_get_all_bookings_ids(api_client, create_booking):
    response = api_client.get(ENDPOINT)
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_bookings_ids_schema)
    ids = []
    for booking in actual_response:
        ids.append(booking['bookingid'])
    # можно сделать то же через list comprehension: ids = [booking['bookingid'] for booking in actual_response]
    assert create_booking['bookingid'] in ids
    # проверка уникальности id: API не должен возвращать дубликаты bookingid.
    assert len(ids) == len(set(ids))



@pytest.mark.parametrize('filter_by, filter_data', [("firstname", {"firstname": "Jim"}),
                                                    ("lastname", {"lastname": "Brown"}),
                                                    ("checkin", {"checkin": "2018-01-01"})])
def test_get_bookings_id_filter_by_data(api_client, create_booking, filter_by, filter_data):

    response = api_client.get(ENDPOINT, params=filter_data)
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_bookings_ids_schema)
    ids = [b['bookingid'] for b in actual_response]
    for booking_id in ids[:3]:
        response2 = api_client.get(f'{ENDPOINT}/{booking_id}')
        assert response2.status_code == 200
        actual_response2 = response2.json()
        print(actual_response2)
        if filter_by == 'checkin' or filter_by == 'checkout':
            checkin_value = actual_response2['bookingdates'][filter_by]
            assert checkin_value != "0NaN-aN-aN"
            assert checkin_value >= filter_data[filter_by]
        else:
            assert actual_response2[filter_by] == filter_data[filter_by]


def test_get_bookings_id_filter_by_firstname_and_lastname(api_client, create_booking):
    response = api_client.get(ENDPOINT, params = {'firstname': 'Jim', 'lastname': 'Brown'})
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_bookings_ids_schema)
    ids = [b['bookingid'] for b in actual_response]
    for booking_id in ids[:3]:
        response2 = api_client.get(f'{ENDPOINT}/{booking_id}')
        assert response2.status_code == 200
        actual_response2 = response2.json()
        assert actual_response2['firstname'] == 'Jim'
        assert actual_response2['lastname'] == 'Brown'


def test_get_bookings_id_filter_by_not_existing_first_name(api_client, create_booking):

    response = api_client.get(ENDPOINT, params = {'firstname': 'QAWERTY_NON_EXISTING_NAME_123456'})
    assert response.status_code == 200
    actual_response = response.json()
    assert len(actual_response) == 0


@pytest.mark.xfail(reason="Known issue: invalid checkin date format is ignored")
@pytest.mark.parametrize('date', ['99', '2012', '07.07.2022'])
def test_get_bookings_id_filter_by_invalid_date(api_client, create_booking,date):
    response = api_client.get(ENDPOINT, params = {'checkin': date})
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.xfail(
    reason="Known bug: GET /booking ignores unsupported query parameters"
)
def test_get_bookings_id_filter_by_invalid_params(api_client, create_booking):
    response = api_client.get(ENDPOINT, params={'invalid_params' : 'params'})
    assert response.status_code == 400









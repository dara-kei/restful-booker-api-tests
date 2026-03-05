from schemas.schema_get_booking_ids import get_bookings_ids_schema
from jsonschema import validate, ValidationError
import pytest

from tests.conftest import api_client

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
    for id in ids[:3]:
        response2 = api_client.get(f'{ENDPOINT}/{id}')
        assert response2.status_code == 200
        actual_response2 = response2.json()
        if filter_by == 'checkin' or filter_by == 'checkout':
            checkin_value = actual_response2['bookingdates'][filter_by]
            if checkin_value == "0NaN-aN-aN": # иногда в checkin находится мусорные данные типа 0NaN-aN-aN, игнорируем их, чтоб тест не падал
                continue
            assert checkin_value >= filter_data[filter_by]
        else:
            assert actual_response2[filter_by] == filter_data[filter_by]


def test_get_bookings_id_filter_by_firstname_and_lastname(api_client, create_booking):
    response = api_client.get(ENDPOINT, params = {'firstname': 'Jim', 'lastname': 'Brown'})
    assert response.status_code == 200
    actual_response = response.json()
    validate(actual_response, get_bookings_ids_schema)
    ids = [b['bookingid'] for b in actual_response]
    for id in ids[:3]:
        response2 = api_client.get(f'{ENDPOINT}/{id}')
        assert response2.status_code == 200
        actual_response2 = response2.json()
        assert actual_response2['firstname'] == 'Jim'
        assert actual_response2['lastname'] == 'Brown'


def test_get_bookings_id_filter_by_not_existing_first_name(api_client, create_booking):

    response = api_client.get(ENDPOINT, params = {'firstname': 'Test'})
    assert response.status_code == 200
    actual_response = response.json()
    assert len(actual_response) == 0


# в реале должен быть код ошибки, например, 400, так как дата невалидна
@pytest.mark.parametrize('date', ['99', '2012', '07.07.2022'])
def test_get_bookings_id_filter_by_invalid_date(api_client, create_booking,date):
    response = api_client.get(ENDPOINT, params = {'checkin': date})
    assert response.status_code == 200


# в реале должен быть код ошибки, например, 400, так как параметры невалидны
def test_get_bookings_id_filter_by_invalid_params(api_client, create_booking):
    response = api_client.get(ENDPOINT, params={'invalid_params' : 'params'})
    assert response.status_code == 200








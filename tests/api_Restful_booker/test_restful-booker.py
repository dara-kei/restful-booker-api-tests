import requests
import pytest
from jsonschema import validate, ValidationError
from .schemas import get_bookings_schema




#
# def test_get_one_booking(get_booking_id):
#     response = requests.get(f'https://restful-booker.herokuapp.com/booking/{get_booking_id}')
#     assert response.status_code == 200
#
#
# def test_create_booking():
#     headers = {'Content-Type': 'application/json'}
#     data = {
#         "firstname": "Jim",
#         "lastname": "Brown",
#         "totalprice": 111,
#         "depositpaid": True,
#         "bookingdates": {
#             "checkin": "2018-01-01",
#             "checkout": "2019-01-01"
#         },
#         "additionalneeds": "Breakfast"
#     }
#     response = requests.post('https://restful-booker.herokuapp.com/booking',
#                              json=data,
#                              headers=headers)
#     assert response.status_code == 200
#
#
# def test_update_booking(get_auth_api, get_booking_id):
#     headers = {'Content-Type': 'application/json',
#                'Cookie' : f'token={get_auth_api}'}
#     data = {
#     "firstname" : "James",
#     "lastname" : "Brown",
#     "totalprice" : 111,
#     "depositpaid" : True,
#     "bookingdates" : {
#         "checkin" : "2018-01-01",
#         "checkout" : "2019-01-01"
#     },
#     "additionalneeds" : "Breakfast"
# }
#     response = requests.put(f'https://restful-booker.herokuapp.com/booking/{get_booking_id}',
#                             json=data,
#                             headers=headers)
#     assert response.status_code == 200
#
#
# def test_partial_update_booking(get_auth_api, get_booking_id):
#     headers = {'Content-Type': 'application/json',
#                'Cookie' : f'token={get_auth_api}'}
#     data = {
#         "firstname": "James",
#         "lastname": "Brown"
#     }
#     response = requests.patch(f'https://restful-booker.herokuapp.com/booking/{get_booking_id}',
#                             json=data,
#                             headers=headers)
#     assert response.status_code == 200
#
#
# def test_delete_booking(get_auth_api, get_booking_id):
#     headers = {'Content-Type': 'application/json',
#                'Cookie': f'token={get_auth_api}'}
#     response = requests.delete(f'https://restful-booker.herokuapp.com/booking/{get_booking_id}',
#                                headers=headers)
#     assert response.status_code == 201
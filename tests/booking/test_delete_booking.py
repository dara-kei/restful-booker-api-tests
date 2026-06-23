import pytest


ENDPOINT = 'booking'


def test_delete_booking(api_client, create_booking_for_delete, token):
    headers = {"Cookie" : f"token={token}"}
    response = api_client.delete(f"{ENDPOINT}/{create_booking_for_delete['bookingid']}", headers=headers)
    assert response.status_code == 201 # лучше код 200!


def test_trying_to_delete_booking_without_token(api_client, create_booking, token):
    response = api_client.delete(f"{ENDPOINT}/{create_booking['bookingid']}")
    assert response.status_code == 403


def test_trying_to_delete_booking_with_invalid_token(api_client, create_booking):
    headers = {"Cookie": f"token=123"}
    response = api_client.delete(f"{ENDPOINT}/{create_booking['bookingid']}", headers=headers)
    assert response.status_code == 403


def test_trying_to_delete_not_existing_booking(api_client, token):
    headers = {"Cookie": f"token={token}"}
    response = api_client.delete(f"{ENDPOINT}/999999999", headers=headers)
    assert response.status_code == 405


@pytest.mark.xfail(
    reason="Known bug: DELETE /booking incorrectly processes invalid booking ids and deletes existing booking"
)
@pytest.mark.parametrize(
    "suffix",
    ["abc", ".1"]
)
def test_delete_booking_with_invalid_id(api_client, create_booking_for_delete, token, suffix):

    invalid_id = f"{create_booking_for_delete['bookingid']}{suffix}"

    headers = {"Cookie": f"token={token}"}

    response = api_client.delete(
        f"{ENDPOINT}/{invalid_id}",
        headers=headers
    )
    assert response.status_code == 400

    response2 = api_client.get(
        f"{ENDPOINT}/{create_booking_for_delete['bookingid']}"
    )

    assert response2.status_code == 200
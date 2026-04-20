ENDPOINT = 'booking'


def test_delete_booking(api_client, create_booking, get_token):
    headers = {"Cookie" : f"token={get_token}"}
    response = api_client.delete(f"{ENDPOINT}/{create_booking['bookingid']}", headers=headers)
    assert response.status_code == 201 # лучше код 200!


def test_trying_to_delete_booking_without_token(api_client, create_booking, get_token):
    response = api_client.delete(f"{ENDPOINT}/{create_booking['bookingid']}")
    assert response.status_code == 403

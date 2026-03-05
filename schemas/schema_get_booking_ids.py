get_bookings_ids_schema = {
    'type' : 'array',
    'items': {
        'type': 'object',
        'properties': {
            'bookingid' : {
                'type': 'integer',
            }
        }
    }
}
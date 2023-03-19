from datetime import datetime

from flaskapp.utils.constants import DATETIME_FORMAT


def is_valid(data):
    message = ''
    # Check that some general fields exist
    essential_fields = ['creation_date',
                        'completion_date',
                        'street_address',
                        'zip_code',
                        'request_type']

    if not all(field in data for field in essential_fields):
        message += 'Missing general info'

    # Check that some request-specific fields exist
    if 'request_type' in data:
        if data['request_type'] == 'Abandoned Vehicle Complaint':
            if not all(field in data for field in ['color', 'model', 'license_plate']):
                message += 'Missing vehicle info'

        elif data['request_type'] == 'Garbage Cart Black Maintenance/Replacement':
            if not all(field in data for field in ['number_of_black_carts']):
                message += 'Missing garbage info'

        elif data['request_type'] == 'Graffiti Removal':
            if not all(field in data for field in ['surface_type', 'graffiti_location']):
                message += 'Missing graffiti info'

        elif data['request_type'] == 'Pothole in Street':
            if not all(field in data for field in ['number_of_potholes']):
                message += 'Missing pothole info'

        elif data['request_type'] == 'Rodent Baiting/Rat Complaint':
            if not all(field in data for field in ['premises_baited']):
                message += 'Missing rodent info'

        elif data['request_type'] == 'Sanitation Code Violation':
            if not all(field in data for field in ['nature']):
                message += 'Missing sanitation info'

        elif data['request_type'] == 'Tree Debris':
            if not all(field in data for field in ['debris_location']):
                message += 'Missing debris info'

        elif data['request_type'] == 'Tree Trim':
            if not all(field in data for field in ['tree_location']):
                message += 'Missing trim info'

    # Check date format
    if 'creation_date' in data:
        try:
            datetime.strptime(data['creation_date'], DATETIME_FORMAT)
        except ValueError:
            message += 'Incorrect creation_date format, should be ' + DATETIME_FORMAT

    if 'completion_date' in data:
        try:
            datetime.strptime(data['completion_date'], DATETIME_FORMAT)
        except ValueError:
            message += 'Incorrect completion_date format, should be ' + DATETIME_FORMAT

    return message



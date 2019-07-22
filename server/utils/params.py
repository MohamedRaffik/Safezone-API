timeSpan = {
    'in': 'query',
    'required': False,
    'description': 'Time Span to filter Crime Occurences by',
    'type': 'string',
    'enum': [
        'week', 'month', '3 month', '6 month', '9 month', 'year'
    ],
    'default': 'year'
}

coordinates = {
    'latitude': {
        'in': 'query',
        'required': True,
        'description': 'Latitude of Coordinate',
        'type': 'number',
        'format': 'float'
    },
    'longitude': {
        'in': 'query',
        'required': True,
        'description': 'Longitude of Coordinate',
        'type': 'number',
        'format': 'float'
    }
}

nearby_crime_input = {
    **coordinates,
    'timeSpan': timeSpan
}

nearby_station_input = {
    **coordinates
}

nearby_crime_of_station_input = {
    'id': {
        'in': 'query',
        'required': True,
        'description': 'ID of a Subway Station',
        'type': 'number',
        'format': 'integer'
    },
    'timeSpan': timeSpan
}

route_input = {
    'origin_latitude': { 
        **coordinates['latitude'],
        'description': 'Latitude of Origin Coordinate'
    },
    'origin_longitude': {
        **coordinates['longitude'],
        'description': 'Longitude of Origin Coordinate'
    },
    'dest_latitude': {
        **coordinates['latitude'],
        'description': 'Latitude of Destination Coordinate'
    },
    'dest_longitude': {
        **coordinates['longitude'],
        'description': 'Longitude of Destination Coordinate'
    }
}
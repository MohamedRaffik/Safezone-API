from flask import request, jsonify
from flask_restplus import Resource, Namespace
from server.auth import authenticate
from server.utils.queries import closest_stations, crimes_near_station, Dates
from server.utils.serializers import validate, sanitize
from server.utils.schemas import NearbyStationSchema, NearbyCrimeOfStationSchema
from server.utils.params import nearby_station_input, nearby_crime_of_station_input
from server.utils.models import station, nearby_crime_response
from server.database import db

stations_ns = Namespace('Stations')

@stations_ns.route('/nearby')
@stations_ns.doc(
    description='Provide a list of nearby Subway Stations and its information', 
    params=nearby_station_input,
    responses={400: 'Parameters Error', 401: 'API key is missing or invalid'}
)
class NearbyStations(Resource):
    @stations_ns.doc(security='apikey')
    @authenticate
    @validate(NearbyStationSchema)
    @stations_ns.marshal_list_with(station)
    def get(self):
        stations = closest_stations(
            db, 
            request.args['latitude'],
            request.args['longitude']
        )

        return [
            {
                'id': station['id'],
                'name': station['name'],
                'lines': station['line'].split(' '),
                'latitude': station['latitude'],
                'longitude': station['longitude'],
                'percentile': round(station['percentile'], 2)
            }
            for station in stations
        ]

@stations_ns.route('/nearby_crimes')
@stations_ns.doc(
    description='List Crime Occurrences that are nearby a Subway Station', 
    params=nearby_crime_of_station_input,
    responses={400: 'Parameters Error', 401: 'API key is missing or invalid'}
)
class NearbyCrimesOfStation(Resource):
    @stations_ns.doc(security='apikey')
    @authenticate
    @validate(NearbyCrimeOfStationSchema)
    @sanitize({'timeSpan': 'year'})
    @stations_ns.marshal_with(nearby_crime_response)
    def get(self):
        results = crimes_near_station(
            db, 
            request.args['id'],
            Dates[ request.args['timeSpan'] ]
        )

        crimes = []
        category_counts = {
            'Burglary': 0,
            'Felony Assault': 0,
            'Grand Larceny': 0,
            'Kidnapping': 0,
            'Misdemeanor Assault': 0,
            'Misdemeanor Sex Crimes': 0,
            'Murder': 0,
            'Offenses against Public Order': 0,
            'Petit Larceny': 0,
            'Rape': 0,
            'Robbery': 0,
            'Shootings': 0
        }

        for r in results:
            crimes.append(
                {
                    'date': str(r['crime_date']),
                    'category': r['category'],
                    'ofns_desc': r['ofns_desc'],
                    'pd_desc': r['pd_desc'],
                    'latitude': r['latitude'],
                    'longitude': r['longitude'],
                }
            )
            category_counts[r['category']] += 1

        return {
            'results': crimes,
            'frequencies': category_counts
        }
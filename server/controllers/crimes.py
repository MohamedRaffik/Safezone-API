from flask import request, jsonify
from flask_restplus import Resource, Namespace, fields
from server.auth import authenticate
from server.utils.queries import crimes_near_point, Dates
from server.utils.serializers import validate, sanitize
from server.utils.schemas import NearbyCrimeSchema
from server.utils.params import nearby_crime_input
from server.utils.models import nearby_crime_response
from server.database import db

crimes_ns = Namespace('Crimes')

@crimes_ns.route('/nearby')
@crimes_ns.doc(
    description='List Crime Occurrences with 500 Ft of the given coordinate',
    params=nearby_crime_input,
    responses={400: 'Parameters Error', 401: 'API key is missing or invalid'}
)
class NearbyCrimes(Resource):
    @crimes_ns.doc(security='apikey')
    @authenticate
    @validate(NearbyCrimeSchema)
    @sanitize({'timeSpan': 'year'})
    @crimes_ns.marshal_with(nearby_crime_response)
    def get(self):        
        results = crimes_near_point(
            db, 
            request.args['latitude'], 
            request.args['longitude'], 
            Dates[ request.args['timeSpan'] ]
        )

        crimes = []
        category_counts = {
            'Murder': 0,
            'Rape': 0,
            'Robbery': 0,
            'Felony Assault': 0,
            'Burglary': 0,
            'Grand Larceny': 0,
            'Petit Larceny': 0,
            'Misdemeanor Assault': 0,
            'Misdemeanor Sex Crimes': 0,
            'Kidnapping': 0,
            'Offenses against Public Order': 0,
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
                    'longitude': r['longitude']
                }
            )
            category_counts[r['category']] += 1

        return {
            'frequencies': category_counts,
            'results': crimes,
        }
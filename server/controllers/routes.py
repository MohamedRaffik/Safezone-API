from flask import request, jsonify
from flask_restplus import Resource, Namespace
from server.auth import authenticate
from server.utils.queries import closest_stations
from server.utils.serializers import validate, sanitize
from server.utils.schemas import RouteSchema
from server.utils.params import route_input
from server.utils.models import route
from server.database import db
from requests import get
from os import getenv

routes_ns = Namespace('Routes')

@routes_ns.route('/')
@routes_ns.doc(
    description='Gives Directions with Safety Ratings from a given Origin to a Destination', 
    params=route_input,
    responses={400: 'Parameters Error', 401: 'API key is missing or invalid'}
)
class Route(Resource):
    def directions(self, origin, destination) -> str:
            origin     : str = f'{origin["latitude"]},{origin["longitude"]}'
            destination: str = f'{destination["latitude"]},{destination["longitude"]}'
            parameters : str = f'origin={origin}&destination={destination}&key={getenv("G_API_KEY")}'
            url        : str = f'https://maps.googleapis.com/maps/api/directions/json?{parameters}&mode=transit&transit_mode=subway&alternatives=true'
            return url

    @routes_ns.doc(security='apikey')
    @authenticate
    @validate(RouteSchema)
    @routes_ns.marshal_list_with(route)
    def get(self):
        gmap_request = get( 
            self.directions(
                { 'latitude': request.args['origin_latitude'], 'longitude': request.args['origin_longitude'] },
                { 'latitude': request.args['dest_latitude'], 'longitude': request.args['dest_longitude'] }
            )
        )

        if gmap_request.status_code != 200:
            return {
                'error': 'Not able to generate route'
            }, 400

        data = gmap_request.json()

        steps_rating = lambda dest, arrive: ( closest_stations(db, dest['location']['lat'], dest['location']['lng'])[0]['percentile'] + 
        closest_stations(db, arrive['location']['lat'], arrive['location']['lng'])[0]['percentile'] ) / 2

        routes = []

        for route in data['routes']:
            for leg in route['legs']:
                rating, count, lines = 0, 0, []
                for step in leg['steps']:
                    if step['travel_mode'] == 'TRANSIT':
                        if step['transit_details']['line']['vehicle']['type'] == 'SUBWAY':
                            details = step['transit_details']
                            departure_stop, arrival_stop = details['departure_stop'], details['arrival_stop']
                            rating, count = rating + steps_rating(departure_stop, arrival_stop), count + 1
                            lines.append(
                                { 
                                    'line': step['transit_details']['line']['short_name'], 
                                    'direction': 'Towards {}'.format(step['transit_details']['headsign'])
                                }
                            )
                routes.append({
                    'rating': round( rating / count, 2 ) if count != 0 else 0,
                    'leg': leg,
                    'lines': lines
                })

        routes.sort(key=lambda x: x['rating'], reverse=True)
        return routes
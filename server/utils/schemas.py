from marshmallow import Schema, fields, ValidationError, validates, validate
from os import getenv
from server.utils.params import timeSpan

class AuthSchema(Schema):
    API_KEY = fields.String(required=True)

    @validates('API_KEY')
    def validate_key(self, key):
        if key != getenv('API_KEY'):
            raise ValidationError('Not Authorized')

class TimeSchema(Schema):
    timeSpan = fields.String(required=False, default=timeSpan['enum'][-1])

    @validates('timeSpan')
    def validate_time(self, time):
        if time not in timeSpan['enum']:
            raise ValidationError('Not a valid time range')

class CoordinateSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

class RouteSchema(AuthSchema):
    origin_latitude = fields.Float(required=True)
    origin_longitude = fields.Float(required=True)
    dest_latitude = fields.Float(required=True)
    dest_longitude = fields.Float(required=True)

    
class NearbyCrimeSchema(AuthSchema, CoordinateSchema, TimeSchema):
    pass

class NearbyStationSchema(AuthSchema, CoordinateSchema):
    pass

class NearbyCrimeOfStationSchema(AuthSchema, TimeSchema):
    id = fields.Integer(required=True, description='ID of a Subway Station')



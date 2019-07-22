from marshmallow import Schema, fields, ValidationError, validates
from flask import request
from os import getenv
from functools import wraps
from server.utils.schemas import AuthSchema

def authenticate(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        schema = AuthSchema()
        errors = schema.validate(request.args)
        if errors.get('API_KEY', None):
            return {
                'error': f'API_KEY {errors["API_KEY"][0]}'
            }, 401
        return f(*args, **kwargs)
    return decorator_function

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'query',
        'name': 'API_KEY'
    }
}
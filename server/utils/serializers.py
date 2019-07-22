from functools import wraps
from flask import request

def validate(Schema):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            schema = Schema()
            errors = list(schema.validate(request.args).items())
            if len(errors) > 0:
                arg, error = errors[0]
                return {
                    'error': f'{arg} {error[0]}'
                }, 400
            return f(*args, **kwargs)
        return decorator_function
    return decorator

def sanitize(params):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            request.args = {
                **request.args,
                **{
                    param: default_value
                    for param, default_value in params.items()
                    if param not in request.args
                }
            }
            return f(*args, **kwargs)
        return decorator_function
    return decorator
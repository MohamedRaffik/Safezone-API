from flask_restplus import fields, Model

frequencies = Model('Frequencies',
    {
        'Burglary': fields.Float,
        'Felony Assault': fields.Float,
        'Grand Larceny': fields.Float,
        'Kidnapping': fields.Float,
        'Misdemeanor Assault': fields.Float,
        'Misdemeanor Sex Crimes': fields.Float,
        'Murder': fields.Float,
        'Offenses against Public Order': fields.Float,
        'Petit Larceny': fields.Float,
        'Rape': fields.Float,
        'Robbery': fields.Float,
        'Shootings': fields.Float
    }
)

crime = Model('Crime', 
    {
        'category': fields.String,
        'date': fields.String,
        'latitude': fields.Float,
        'longitude': fields.Float,
        'ofns_desc': fields.String,
        'pd_desc': fields.String
    }
)

station = Model('Station', 
    {
        'id': fields.Integer,
        'latitude': fields.Float,
        'longitude': fields.Float,
        'lines': fields.List(fields.String),
        'name': fields.String,
        'percentile': fields.Float
    }
)

line = Model('Line', 
    {
        'direction': fields.String,
        'line': fields.String
    }
)

route = Model('Route', 
    {
        'leg': fields.Raw,
        'lines': fields.List( fields.Nested(line) ),
        'rating': fields.Float
    }
)

nearby_crime_response = Model('NearbyCrimeResponse', 
    {
        'frequencies': fields.Nested(frequencies),
        'results': fields.List(fields.Nested(crime))
    }
)

def register_models(api):
    models = [
        frequencies,
        crime, 
        station,
        line,
        route,
        nearby_crime_response
    ]
    for model in models:
        api.models[model.name] = model
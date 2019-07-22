from flask import Flask, Blueprint, redirect
from flask_cors import CORS
from flask_restplus import Api, Resource
from server.auth import authorizations
from server.controllers.crimes import crimes_ns
from server.controllers.routes import routes_ns
from server.controllers.stations import stations_ns
from server.utils.models import register_models

def create_app():

    app = Flask(__name__)

    app.config['RESTPLUS_MASK_SWAGGER'] = False

    blueprint = Blueprint('api', __name__, url_prefix='/api')

    api = Api(
        blueprint, 
        version='1.0', 
        title='SafeZone API', 
        authorizations=authorizations,
        doc='/ui/'
    )

    register_models(api)

    app.register_blueprint(blueprint)

    api.add_namespace(crimes_ns, '/crimes')
    api.add_namespace(stations_ns, '/stations')
    api.add_namespace(routes_ns, '/route')

    @app.route('/')
    def index():
        return redirect('/api/ui')

    CORS(app)

    return app
from system.model import db, app
import simplejson as json
from sqlalchemy.exc import IntegrityError
from resources.user import UserResource, UserCollection
from flask_restful import Api
import database.db
import system.responces.api_response as response
from flask_jwt import JWT, jwt_required, current_identity
from system.auth import Auth, jwt
from system.config import config
from flask_swagger_ui import get_swaggerui_blueprint
import os


SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:5000/swagger'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "API Documentation"
    },
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Initialize Flask api
db.init_app(app)
api = Api(app,prefix=config["api_prefix"])

api.add_resource(UserResource, '/users/<user_id>')
api.add_resource(UserCollection, '/users')
api.add_resource(Auth, '/register')


@app.route('/')
def index():
    return response.view({
        'info': "Flask REST API",
    },200)

### Return Swagger Json file
@app.route('/swagger')
def swagger():
    with open("api/swagger.json", "r") as f:
        content = f.read()
    return content

@app.route(config["api_prefix"]+'/migrate')
#@jwt_required()
def migrateTables():
    try:
        db.create_all()
        return response.view({'status': True},200)
    except IntegrityError:
        return json.dumps({'status': False})


### Set custom header to all responses
# @app.after_request
# def apply_caching(response):
#     response.headers["Content-Type"] = "application/json"
#     return response

### Handle 404 exception
@app.errorhandler(404)
def page_not_found(e):
    return response.errorView("Page not found",404)

# Start REST API flask service
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)

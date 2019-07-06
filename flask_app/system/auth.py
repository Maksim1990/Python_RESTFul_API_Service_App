from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from resources.user import User as userAuth, get_request_args
from system.model import app, db
import hashlib
import system.responces.api_response as response
from system.config import config
from flask_restful import Resource
import datetime

# Login authentication logic
def authenticate(email, password):
    user = userAuth.query.filter_by(email=email).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), hashlib.md5(password.encode('utf-8')).hexdigest()):
        return user

def identity(payload):
    user_id = payload['identity']
    return userAuth.query.filter_by(id=user_id).first()


app.config['SECRET_KEY'] = config["secret_key"]
app.config['JWT_AUTH_HEADER_PREFIX'] = config["jwt_auth_header_prefix"]
app.config['JWT_AUTH_URL_RULE'] = config["api_prefix"]+'/login'
app.config['JWT_EXPIRATION_DELTA'] = config["token_expiration_time"]
jwt = JWT(app, authenticate, identity)


# User collection class
class Auth(Resource):
    def post(self):
        return register_user()

def register_user():
    args = get_request_args()
    if not args['username']:
        return response.errorView("Username should be provided",400)
    elif not args['email']:
        return response.errorView("Email should be provided",400)
    elif not args['password']:
        return response.errorView("Password should be provided",400)
    else:
        user = userAuth(args['username'],
                    hashlib.md5(args['password'].encode('utf-8')).hexdigest(),
                    args['email'],
                    args['phone'],
                    datetime.datetime.now()
                    )
        db.session.add(user)
        db.session.commit()
        return response.view({'status': 'Successfully created!'},200)

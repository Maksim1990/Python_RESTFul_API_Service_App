from flask_restful import reqparse, Resource, abort
from flask_jwt import JWT, jwt_required, current_identity
import system.responces.api_response as response
from system.model import db
from functools import wraps


def checkuser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = User.query.filter_by(id=current_identity.id).first()
        if user:
            return func(*args, **kwargs)
        return response.errorView('Not authenticated',401)
    return wrapper


class User(db.Model):
	# Data Model User Table
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=False)
	password = db.Column(db.String(80), unique=False)
	email = db.Column(db.String(120), unique=True)
	phone = db.Column(db.String(120), unique=False,nullable=True)
	created_at = db.Column(db.DateTime, unique=False,nullable=True)

	def __init__(self, username,password, email, phone, created_at):
		# Initialize columns
		self.username = username
		self.password = password
		self.email = email
		self.phone = phone
		self.created_at = created_at

	def __repr__(self):
		return '<User %r>' % self.username

# User resource class
class UserResource(Resource):
    decorators = [checkuser, jwt_required()]
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return response.errorView('User not found',404)
        data=  {'username':user.username,'email': user.email, 'phone': user.phone, 'created_at': user.created_at.__str__()}
        return response.view(data,200)

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return response.errorView('User not found',404)
        db.session.delete(user)
        db.session.commit()
        return response.view('User deleted',200)

    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return response.errorView('User not found',404)
        args = get_request_args()
        if args:
            for key, value in args.items():
                if not value:
                    continue
                setattr(user, key, value)
        db.session.commit()
        return response.view("Updated",201)

# User collection class
class UserCollection(Resource):
    decorators = [checkuser, jwt_required()]
    def get(self):
        users = User.query.all()
        users_dict = []
        for user in users:
                users_dict.append({
                    'id':user.id,
                    'username':user.username,
                    'email': user.email,
                    'phone': user.phone,
                    'created_at': user.created_at.__str__()
                })
        return response.view(users_dict,200)


def get_request_args():
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('email')
    parser.add_argument('phone')
    return parser.parse_args()



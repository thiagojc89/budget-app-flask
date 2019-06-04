import json
import models
from flask import jsonify, Blueprint, abort, make_response
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with




user_fields = {
	'first_name': fields.String,
	'last_name':fields.String,
	'email':fields.String,
	'password':fields.String,
	'created_at':fields.String
}


class User(Resource):
    def __init__(self):
	    self.reqparse = reqparse.RequestParser()
	    self.reqparse.add_argument(
	        'first_name',
	        required=False,
	        help='No first name provided',
	        location=['form', 'json']
	    )
	    self.reqparse.add_argument(
	        'last_name',
	        required=False,
	        help='No last name provided',
	        location=['form', 'json']
	    )
	    self.reqparse.add_argument(
	        'email',
	        required=False,
	        help='No email provided',
	        location=['form', 'json']
	    )
	    self.reqparse.add_argument(
	        'password',
	        required=False,
	        help='No password provided',
	        location=['form', 'json']
	    )

	    super().__init__()

    def post(self):
    	print('hit post route create user')
    	args = self.reqparse.parse_args()
    	user = 	models.User.create_user(**args)
    	login_user(user)
    	return marshal(user, user_fields), 201



class Login(Resource):
    def __init__(self):
	    self.reqparse = reqparse.RequestParser()
	    self.reqparse.add_argument(
	        'first_name',
	        required=False,
	        help='No first name provided',
	        location=['form', 'json']
	    )
	    self.reqparse.add_argument(
	        'last_name',
	        required=False,
	        help='No last name provided',
	        location=['form', 'json']
	    )
	    self.reqparse.add_argument(
	        'email',
	        required=False,
	        help='No email provided',
	        location=['form', 'json']
	    )
	    self.reqparse.add_argument(
	        'password',
	        required=False,
	        help='No password provided',
	        location=['form', 'json']
	    )
	    super().__init__()

    
    def post(self):
    	
    	args = self.reqparse.parse_args()
    	try:
    		user = models.User.get(models.User.email==args.email)
    	except models.User.DoesNotExist:
    		abort(404)
    	else:
    		
    		if check_password_hash(user.password, args.password):
    			login_user(user)
    			return marshal(user,user_fields), 200
    		else:
    			return ('User or Password is invalid')
        

auth_api = Blueprint('resources.auth', __name__)
api = Api(auth_api)

api.add_resource(
	User,
	'/register'
)
api.add_resource(
	Login,
	'/login'
)
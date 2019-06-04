import json
import models
from flask import jsonify, Blueprint, abort, make_response
from flask_login import login_required, current_user
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with


class User(Resource):
	def __init__(self):
		print('not now')
	
	# super().__init__()
	
	def get(self):
		print('GET Route')
		return 'YOU HIT THE GET ROUTE'

	def post(self):
		print('POST Route')
		return 'YOU HIT THE POST ROUTE'

	def put(self):
		print('PUT Route')
		return 'YOU HIT THE PUT ROUTE'

	def delete(self):
		print('DESTROY Route')
		return 'YOU HIT THE DELETE ROUTE'

user_api = Blueprint('resource.user', __name__)
api = Api(user_api)

api.add_resource(
	User,
	'/budgetitem'
)
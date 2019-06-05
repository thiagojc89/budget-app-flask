import json
import models
from flask import jsonify, Blueprint, abort, make_response, request, g
from flask_login import login_required, current_user
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

itens_fields = {
	"id": fields.String,
    "name": fields.String,
    "value": fields.String,
    "due_date": fields.String,
    "payment_date": fields.String,
    "transaction": fields.String,
    "user_id": fields.String,
    "budget_id": fields.String
}

class User(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=False,
			help='No first name provided',
			location=['form', 'json'])
		self.reqparse.add_argument(
			'value',
			required=False,
			help='No value provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'due_date',
			required=False,
			help='No due_date provided',
			location=['form', 'json'])
		self.reqparse.add_argument(
			'payment_date',
			required=False,
			help='No payment_date provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'transaction',
			required=False,
			help='No transaction provided',
			location=['form', 'json']
		)
		super().__init__()
	
	def get(self):
		print('GET Route')
		return 'YOU HIT THE GET ROUTE'
	@marshal_with(itens_fields)
	def post(self):
		print('POST Route')
		args = self.reqparse.parse_args()
		args.user_id=g.user._get_current_object().id
		args.budget_id=request.args.get('budget_id')

		item = models.Item.create(**args)

		return item, 200

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
# create a route to get all user info instead of using this.state [... spread operator].




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
		# budget_id is passing as a params
		# user_id = request.args.get('user_id')
		user_id = g.user._get_current_object().id

		itens = (models.Item
			.select()
			# .select(models.Budget, models.Item)
			.join(models.Budget)
			.dicts()
			.where(models.Budget.user_id==user_id)
		)
		itens = [marshal(item ,itens_fields) for item in itens]
		return itens, 200


	@marshal_with(itens_fields)
	def post(self):
		# I'm taking the user from the session "current_user"
		# getting the budget_id from the query params call budget_id
		args = self.reqparse.parse_args()
		args.user_id=g.user._get_current_object().id
		args.budget_id=request.args.get('budget_id')
		item = models.Item.create(**args)

		return item, 200

	@marshal_with(itens_fields)
	def put(self):
		# item_id is passing as a params
		item_id = request.args.get('item_id')
		args = self.reqparse.parse_args()

		item_args = {}

		if args['name'] != None:
			item_args['name'] = args['name']

		if args['value'] != None:
			item_args['value'] = args['value']

		if args['due_date'] != None:
			item_args['due_date'] = args['due_date']

		if args['payment_date'] != None:
			item_args['payment_date'] = args['payment_date']

		if args['transaction'] != None:
			item_args['transaction'] = args['transaction']

		print('this is what I\'m going to update ', item_args)


		query = models.Item.update(**item_args).where(models.Item.id==item_id)
		query.execute()
		return models.Item.get(models.Item.id==item_id), 200


	def delete(self):
		# item_id is passing as a params
		item_id = request.args.get('item_id')
		query = models.Item.delete().where(models.Item.id==item_id)
		query.execute()
		return 'YOU HIT THE DELETE ROUTE and destroy the item'

user_api = Blueprint('resource.user', __name__)
api = Api(user_api)

api.add_resource(
	User,
	'/budgetitem'
)
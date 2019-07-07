# create a route to get all user info instead of using this.state [... spread operator].
# Overall, I love this cover letter. It's warm and engaging. Go with it for this job! For future cover letters, It is a little on the long side, and I want to see more customization to the job you are applying to - meaning I want to see you mention something about what they are looking for in the job description and then make a clear connection between that and what skills and experience you have. I don't get that from this cover letter. Still, I think this one is good to go and I think you should get it out the door ASAP! :)


import datetime
import json
import models
from flask import jsonify, Blueprint, abort, make_response, request, g
from flask_login import login_required, current_user
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

itens_fields = {
	"id": fields.String,
    "name": fields.String,
    "value": fields.Price(decimals=2),
    "due_date": fields.String,
    "payment_date": fields.String,
    # "due_date": fields.DateTime(dt_format='iso8601'),
    # "payment_date": fields.DateTime(dt_format='iso8601'),
    # "due_date": fields.DateTime(dt_format='rfc822'),
    # "payment_date": fields.DateTime(dt_format='rfc822'),
    "transaction": fields.String,
    "user_id": fields.String,
    "budget_id": fields.String,
    "created_at": fields.DateTime
    # "created_at": fields.String
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
			.select(models.Item)
			# .select(models.Budget, models.Item)
			.join(models.Budget)
			.where(models.Budget.user_id==user_id)
			.order_by(models.Item.payment_date))
		# converting the date(string) from the DB to a date datatype

		# for i in itens:
		# 	# print('this is the ITENS >>>> ',i.due_date)
		# 	# print('this is the ITENS >>>> ',i.payment_date)
		# 	# print('this is the ITENS >>>> ',type(i.payment_date))
		# 	# print('this is the ITENS >>>> ',type(i.payment_date))

		# 	i.due_date = datetime.datetime.strptime(i.due_date, '%Y-%m-%d')
		# 	i.payment_date = datetime.datetime.strptime(i.payment_date, '%Y-%m-%d')

		itens = [marshal(item ,itens_fields) for item in itens]
		return itens, 200


	@marshal_with(itens_fields)
	def post(self):
		# I'm taking the user from the session "current_user"
		# getting the budget_id from the query params call budget_id
		args = self.reqparse.parse_args()

		user_id = g.user._get_current_object().id
		print('my user is >>>>>', user_id)

		args.user_id=g.user._get_current_object().id
		# args.budget_id=request.args.get('budget_id')

		budget_id = models.Budget.get(models.Budget.user_id==user_id)

		print('this is my budget id >>>>>> ', budget_id)


		args.budget_id = budget_id
		
		
		item = models.Item.create(**args)

		
		# converting the date(string) from the DB to a date datatype
		item.due_date = datetime.datetime.strptime(item.due_date, '%Y-%m-%d')
		item.payment_date = datetime.datetime.strptime(item.payment_date, '%Y-%m-%d')
		


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
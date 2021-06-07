import datetime
import json
import models
from flask import jsonify, Blueprint, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

user_api = Blueprint('user', __name__)

@user_api.get('/budgetitem')
def get_budget_items():

	items = (models.Item.select(models.Item)
		.join(models.Budget)
		.where(models.Budget.user_id==current_user)
		.order_by(models.Item.payment_date))

	items_list = [model_to_dict(item) for item in items]
	return jsonify(items_list), 200


@user_api.post('/budgetitem')
def create_item():
	payload = request.get_json()

	budget_id = models.Budget.get(models.Budget.user_id==current_user.id)

	payload['budget_id'] = budget_id
	payload['user_id'] = current_user.id
	
	item = models.Item.create(**payload)
	
	item.due_date = datetime.datetime.strptime(item.due_date, '%Y-%m-%d')
	item.payment_date = datetime.datetime.strptime(item.payment_date, '%Y-%m-%d')
	
	return model_to_dict(item), 200

@user_api.put('/budgetitem')
def update_item():
	item_id = request.args.get('item_id')
	payload = request.get_json()

	item_payload = {}

	if payload['name'] != None:
		item_payload['name'] = payload['name']

	if payload['value'] != None:
		item_payload['value'] = payload['value']

	if payload['payment_date'] != None:
		item_payload['payment_date'] = payload['payment_date']

	if payload['transaction'] != None:
		item_payload['transaction'] = payload['transaction']


	query = models.Item.update(**item_payload).where(models.Item.id==current_user.id)
	query.execute()
	return jsonify(model_to_dict(models.Item.get(models.Item.id==item_id))), 200


@user_api.delete('/budgetitem')
def delete():
	item_id = request.args.get('item_id')
	query = models.Item.delete().where(models.Item.id==item_id)
	query.execute()
	return 'YOU HIT THE DELETE ROUTE and destroy the item'



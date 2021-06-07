import json
import models
import datetime as dt
from flask import jsonify, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from playhouse.shortcuts import model_to_dict

auth_api = Blueprint('auth', __name__)

@auth_api.post('/register')
def register():
	print('hit the register route')
	payload = request.get_json()
	user = 	models.User.create_user(**payload)
	login_user(user)
	
	budget_info={
		'user_id': user.id,
		'name': dt.datetime.now().strftime("%B"),
		'start_date': dt.datetime.now(),
		'end_date': dt.datetime.now()
	}

	budget = models.Budget.create(**budget_info)

	user_dict = model_to_dict(user)
	budget_dict = model_to_dict(budget)

	return jsonify(*user_dict, *budget_dict), 201


@auth_api.post('/login')
def login():
	
	payload = request.get_json()
	try:
		user = models.User.get(models.User.email==payload['email'])
	except models.User.DoesNotExist:
		return 'User not found'
	else:	
		if check_password_hash(user.password, payload['password']):
			login_user(user)
			return model_to_dict(user), 200
		else:
			return 'User or Password is invalid'


@auth_api.get('/logout')
def logout():
	logout_user()
	return jsonify(msg='user logout')


@auth_api.get('/login')
def check_login():
	if current_user.is_authenticated:
		return jsonify(['true', model_to_dict(current_user)])
	else:
		return jsonify(['false'])
	

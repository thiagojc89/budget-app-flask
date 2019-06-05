import datetime

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


import os
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
	import config
	DATABASE = SqliteDatabase(config.DATABASE)

class User(UserMixin, Model): 
    id              = PrimaryKeyField(null=False)
    first_name      = CharField()
    last_name       = CharField()
    email           = CharField()
    password        = CharField()
    balance			= CharField(default='00,00')
    created_at		= DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, first_name, last_name, email, password, **kwargs):
        try:
            cls.select().where(
                (cls.email==email)
                ).get()
        except cls.DoesNotExist:
        	print('>>>>>>>> going to create new user <<<<<<<<<<')
        	user = cls(first_name=first_name, last_name=last_name, email=email, password=password)
        	user.password = generate_password_hash(password)
        	user.save()
        	return user
        else:
        	raise Exception("User with that email address already exists")



class Budget(Model):
    id              = PrimaryKeyField(null=False) 
    user_id			= ForeignKeyField(User, related_name='user')
    name            = CharField()
    start_date		= CharField()
    end_date		= CharField()
    created_at      = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
    

class Item(Model):
    id              = PrimaryKeyField(null=False)
    user_id         = ForeignKeyField(User, related_name='user')
    budget_id       = ForeignKeyField(Budget, related_name='budget')
    name 			= CharField()
    value			= CharField()
    due_date		= CharField()
    payment_date	= CharField()
    transaction		= CharField()
    created_at      = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
  

def initialize(): 
    DATABASE.connect()
    DATABASE.create_tables([User, Budget, Item], safe=True)
    DATABASE.close()
from flask import Flask, g
from flask_login import LoginManager, current_user
from flask_cors import CORS
# import config
import models
from resources.auth import auth_api
from resources.user import user_api
import os

app = Flask(__name__)


# app.config.from_pyfile('config.py')


login_manager = LoginManager()
login_manager.init_app(app)


app.secret_key = 'jasdlfj.adsfjlajr2345458dsf.adsjflkadsf'



@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None


CORS(auth_api, origins=["http://localhost:3000", "https://moneychart.herokuapp.com"], supports_credentials=True)
CORS(user_api, origins=["http://localhost:3000", "https://moneychart.herokuapp.com"], supports_credentials=True)


app.register_blueprint(auth_api, url_prefix='/api/v1/auth')
app.register_blueprint(user_api, url_prefix='/api/v1/user')


@app.before_request
def before_request():

    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response



@app.route('/')
def get():
	return 'Hello World!'


print(__name__, "this is the name o the app")
print(os.environ,"this is the ENV")
if __name__ == 'app':

	if 'ON_HEROKU' in os.environ:
	    print('hitting ')
	    print('hitting ')
	    print('hitting ')
	    print('hitting ')
	    print('hitting ')
	    # models.initialize()
	print("we are just about to call the DB and run the app")
	models.initialize()
	app.run()




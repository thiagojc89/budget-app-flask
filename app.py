from dotenv import load_dotenv
load_dotenv() # takes the environment variables from .env
from flask import Flask
from flask_login import LoginManager, current_user
from flask_cors import CORS
from resources.auth import auth_api
from resources.user import user_api
import os
import models


app = Flask(__name__)


app.secret_key = os.environ.get("SECRET_KEY") ## Need this to encode the session
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


CORS(auth_api, origins=["http://localhost:3000", "https://moneychart.herokuapp.com"], supports_credentials=True)
CORS(user_api, origins=["http://localhost:3000", "https://moneychart.herokuapp.com"], supports_credentials=True)


app.register_blueprint(auth_api, url_prefix='/api/v1/auth')
app.register_blueprint(user_api, url_prefix='/api/v1/user')


@app.before_request
def before_request():
    models.DATABASE.connect()


@app.after_request
def after_request(response):
    models.DATABASE.close()
    return response

@app.route('/')
def get():
	return 'Hello World!'


if 'ON_HEROKU' in os.environ:
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(port=os.environ.get('PORT'), debug=os.environ.get('DEBUG'))


from flask import Flask

import config

import models
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = config.SECRET_KEY




@app.route('/')
def get():
	return 'Hello World!'



if __name__ == '__main__':
	app.run(debug=config.DEBUG, port=config.PORT)




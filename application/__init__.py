from flask import Flask
from flask_cors import CORS
# from flask_pymongo import PyMongo
from application import config

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
# app.config['MONGO_URI'] = config.MONGO_URI

# mongo_client = PyMongo(app)
# db = mongo_client.db
CORS(app, resources={ r"/api/*": { "origins": "*" } })

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

from application import routes
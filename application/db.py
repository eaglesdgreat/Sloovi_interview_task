from flask import Flask
from flask_pymongo import pymongo
from application import app, config


CONNECTION_STRING = config.MONGO_URI
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database(config.MONGO_DATABASE)
user_collection = pymongo.collection.Collection(db, 'users')
template_collection = pymongo.collection.Collection(db, 'templates')
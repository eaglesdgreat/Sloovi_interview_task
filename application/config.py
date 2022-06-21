import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', None)
MONGO_USER = os.environ.get('MONGO_USER', None)
MONGO_DATABASE = os.environ.get('MONGO_DATABASE')
MONGO_URI = "mongodb+srv://%s:%s@cluster0.c4wyt.mongodb.net/%s?retryWrites=true&w=majority" % (
    MONGO_USER,
    MONGO_PASSWORD,
    MONGO_DATABASE
)
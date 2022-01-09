import os
from pymongo import MongoClient


URI = 'mongodb://' \
    + os.environ.get('MONGODB_USERNAME') \
    + ':' \
    + os.environ.get('MONGODB_PASSWORD') \
    + '@' \
    + os.environ.get('MONGODB_HOSTNAME') \
    + ':27017/' \
    + os.environ.get('MONGODB_DATABASE')

# db_name = os.environ['MONGO_INITDB_DATABASE']

def get_db():
    return MongoClient(URI)
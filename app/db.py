import os
from pymongo import MongoClient


URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
db_name = os.environ['MONGO_INITDB_DATABASE']
client = MongoClient(URI)

def get_db():
    return client[db_name]
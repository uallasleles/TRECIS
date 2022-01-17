import os
from pymongo import MongoClient


def get_db():
    client = MongoClient()
    URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
    client = MongoClient(URI)
    return client.carsdb
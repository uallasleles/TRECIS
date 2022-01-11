#!/usr/bin/env python
import os
import requests
import urllib.parse
import pprint
from datetime import datetime
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri


application = Flask(__name__)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
mongo = PyMongo(application)
db = mongo.db

# username        = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
# password        = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
# hostname        = urllib.parse.quote_plus(os.environ['MONGODB_HOSTNAME'])
# database        = urllib.parse.quote_plus(os.environ['MONGODB_DATABASE'])
# authSource      = urllib.parse.quote_plus(os.environ['MONGODB_DATABASE'])
# authMechanism   = urllib.parse.quote_plus('DEFAULT')
# uri = "mongodb://" + username + ":" + password + "@" + hostname + "/"+ database
# # +"?authSource=" + authSource + "&authMechanism=" + authMechanism
# client = MongoClient(uri)
# db = client.get_database()


@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app!'
    )

@application.route('/plate')
def plate():
    _plates = db.plate.find()

    item = {}
    data = []

    for plate in _plates:
        item = {
            'id':                   str(plate['_id']),
            'plate':                plate['plate']['plate'],
            'confidence':           plate['plate']['confidence'],
            'processing_time_ms':   plate['plate']['processing_time_ms'],
            'coordinates':          plate['plate']['coordinates']
        }
        data.append(item)
    
    return jsonify(
        status=True,
        data=data
    )

@application.route('/plate', methods=['POST'])
def addPlate():
    data = request.get_json(force=True)
    item = {
        'plate': data['plate']
    }
    db.plate.insert_one(item)

    return jsonify(
        status=True,
        message='License Plate registred successfully!'
    ), 201

@application.route('/send')
def sendAPI():
    filter = {}
    project = {
        '_id': True,
        'plate.epoch_time': True, 
        'plate.img_height': True, 
        'plate.img_width': True, 
        'plate.results.plate': True, 
        'plate.results.confidence': True, 
        'plate.results.coordinates.x': True, 
        'plate.results.coordinates.y': True, 
        'plate.results.vehicle_region.x': True, 
        'plate.results.vehicle_region.y': True, 
        'plate.results.vehicle_region.height': True, 
        'plate.results.vehicle_region.width': True
    }
    
    data = []
    
    result = db.plate.find(
        filter=filter,
        projection=project
    )

    for i, j in enumerate(result):
        item = {
            '_id':          result[i]['_id'],
            'epoch_time':   result[i]['plate']['epoch_time'],
            'confidence':   result[i]['plate']['results']['confidence'],
            'plate':        result[i]['plate']['results']['plate']
        }
        data.append(item)
   
    return jsonify(
        status=True,
        data=data
    )

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
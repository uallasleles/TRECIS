#!/usr/bin/env python
import os
import time
import requests
import urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from pprint import pprint
from logging import exception


# TODO Mudar o Client para a lib PyMongo em vez da Flask_PyMongo
application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
mongo = PyMongo(application)
db = mongo.db

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
            'epoch_time':           plate['plate']['epoch_time'],
            'img_height':           plate['plate']['img_height'],
            'img_width':            plate['plate']['img_width'],
            'confidence':           plate['plate']['results'][0]['confidence'],
            'coordinates_xy1':      plate['plate']['results'][0]['coordinates'][0],
            'coordinates_xy2':      plate['plate']['results'][0]['coordinates'][1],
            'coordinates_xy3':      plate['plate']['results'][0]['coordinates'][2],
            'coordinates_xy4':      plate['plate']['results'][0]['coordinates'][3]
        }
        data.append(item)
    
    return jsonify(
        status=True,
        data=data
    )

@application.route('/plate', methods=['POST'])
def add_plate():
    data = request.get_json(force=True)
    item = {
        'plate': data['plate']
    }
    db.plate.insert_one(item)

    return jsonify(
        status=True,
        message='License Plate registred successfully!'
    ), 201

@application.route('/query_doc/<string:doc_id>')
def query_doc(doc_id):

    filter = {'_id.$': ObjectId(doc_id)}
    projection = {'_id': True, 'plate.results.plate': True}
    
    try:
        rs = db.plate.find_one(filter=filter, projection=projection)
    except:
        exception("message")

    return jsonify(
        status=True,
        data=rs
    )

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
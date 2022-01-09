#!/usr/bin/env python
import os
from datetime import datetime
from flask import Flask, request, jsonify
from db import get_db


application = Flask(__name__)

db = get_db()

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
            'id': str(plate['_id']),
            'plate': plate['plate']['plate'],
            'confidence': plate['plate']['confidence'],
            'processing_time_ms': plate['plate']['processing_time_ms'],
            'coordinates': plate['plate']['coordinates']
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
def send():
    filter = {}
    project = {
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

    result = db.plate.find(
        filter=filter,
        projection=project
    )
    
    data = []

    # filtro de campos
    for plate in result:
        data.append(plate)
    
    return jsonify(
        status=True,
        data=data
    )

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
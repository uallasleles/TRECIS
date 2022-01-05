#!/usr/bin/env python
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

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

@application.route('/todo')
def todo():
    _todos = db.todo.find()

    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )

@application.route('/todo', methods=['POST'])
def createTodo():
    data = request.get_json(force=True)
    item = {
        'todo': data['todo']
    }
    db.todo.insert_one(item)

    return jsonify(
        status=True,
        message='To-do saved successfully!'
    ), 201

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
            'coordinates': plate['plate']['coordinates'],
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

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
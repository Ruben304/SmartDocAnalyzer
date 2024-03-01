import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/"

    client = MongoClient(app.config["MONGO_URI"])
    app.db = client.doc_analyzer

    app.register_blueprint(main)

    return app
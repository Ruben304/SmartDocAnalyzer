import json
from flask import Flask, jsonify, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS, ALL
from pymongo import MongoClient
from .routes import main

def create_app():
    app = Flask(__name__)

    # configuring flask uploads => enables file upload
    app.config['UPLOADED_FILES_DEST'] = 'uploads'  # Folder where files will be saved!!!!
    app.config['UPLOADED_FILES_ALLOW'] = DOCUMENTS + IMAGES  # allows document and image uploads
    # creates an UploadSet called filea
    files = UploadSet('files', ALL)  # sets an upload set, and allows ALL all file types
    #register upload set with app
    configure_uploads(app, files)


    # configuring MongoDB 
    app.config["MONGO_URI"] = "mongodb://localhost:27017/"
    client = MongoClient(app.config["MONGO_URI"])
    app.db = client.doc_analyzer


    app.register_blueprint(main)

    return app
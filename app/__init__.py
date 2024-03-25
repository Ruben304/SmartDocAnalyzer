import json
from flask import Flask, jsonify, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS, ALL
from pymongo import MongoClient
from celery import Celery
from .routes import main

# Global variable for Celery
celery = None

def make_celery(app):
    celery = Celery(
        app.import_name, 
        backend=app.config['CELERY_RESULT_BACKEND'], 
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
                
    celery.Task = ContextTask
    return celery


def create_app():
    app = Flask(__name__)


    # Celery configurations
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    celery = make_celery(app)


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
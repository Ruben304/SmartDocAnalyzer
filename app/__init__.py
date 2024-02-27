import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doc_api.db'
db = SQLAlchemy(app)

from app import routes


if __name__ == '__main__':
    app.run(debug=True)
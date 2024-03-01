from flask import request, Blueprint, jsonify
from .utils import find_users, insert_user, serialize_doc

# POST = create
# GET = retrieve
# PUT = replace
# DELETE = delete
# PATCH = update

main = Blueprint('main', __name__)
@main.route('/')
def home():
    return "Welcome to my Smart Doc Analyzer 1.0!"

@main.route('/users', methods=['GET'])
def users():
    users = find_users()
    return jsonify(users)

@main.route('/users', methods=['Post'])
def create_user():
    user_data = request.json
    if not user_data:
        return jsonify({"error": "Missing data"}), 400  # Bad request

    result = insert_user(user_data)
    
    if result:
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"error": "Failed to create user"}), 500
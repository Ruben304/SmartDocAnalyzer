from flask import request, Blueprint, jsonify
from .utils import *

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

@main.route('/user', methods=['POST'])
def create_user():
    user_data = request.json
    if not user_data:
        return jsonify({"error": "Missing data"}), 400  # Bad request

    result = insert_user(user_data)
    
    # check for username error 
    if result == "Username already in use.": 
        return jsonify({"error": "Username already in use"}), 409 
    
    if result:
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"error": "Failed to create user"}), 500

@main.route('/user/<username>', methods=['GET'])  
def get_user(username):
    user = find_user(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


@main.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    result = remove_user(username)
    if result:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

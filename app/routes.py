from flask import request, Blueprint, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
from werkzeug.utils import secure_filename
from .utils import *

# POST = create
# GET = retrieve
# PUT = replace
# DELETE = delete
# PATCH = update

documents = UploadSet('files', DOCUMENTS + IMAGES)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Welcome to my Smart Doc Analyzer 2.0!"

@main.route('/users', methods=['GET'])
def users():
    users = find_users()
    return jsonify(users), 200

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

@main.route('/user/<username>/upload', methods=['POST'])
def upload_file(username):
    if 'document' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['document']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    

    if file and documents.file_allowed(file, file.filename):
        filename = secure_filename(file.filename)
        file_url = documents.save(file, name=filename)

        
        insert_document_metadata(username, filename, file_url)
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
    else:
        return jsonify({"error": "File type not allowed"}), 400

@main.route('/documents', methods=['GET'])
def documents(): 
    documents = find_documents()
    return jsonify(documents), 200

@main.route('/user/<username>/documents', methods=['GET'])
def get_user_documents(username):
    user_documents = find_documents_by_username(username)
    if user_documents:
        return jsonify(user_documents), 200
    else:
        return jsonify({"error": "No documents found for this user"}), 404
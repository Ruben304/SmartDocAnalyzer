from flask import current_app as app
from bson import ObjectId
from datetime import datetime
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS


# script for help functions 

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

def find_users():
    users = app.db.users.find({})
    return [serialize_doc(user) for user in users]

def insert_user(user_data):
    try:
        # Check if username already exists
        if app.db.users.find_one({"username": user_data["username"]}):
            print("Username already in use.")
            return "Username already in use."
        
        user_data['time_created'] = datetime.utcnow()
        result = app.db.users.insert_one(user_data)  
        
        return result.inserted_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def find_user(username):
    user = app.db.users.find_one({"username": username})
    if user:
        user['_id'] = str(user['_id'])  # ObjectId to string for JSON serialization
    return user

def remove_user(username):
    result = app.db.users.delete_one({"username": username})
    if result.deleted_count > 0:
        return True
    else:
        return False
    
def insert_document_metadata(username, filename, file_url):
    user = find_user(username)
    doc_metadata = {
        "username_uploaded": username,  # Link to the user's ObjectId or unique identifier
        "userID_uploaded": user['_id'],
        "filename": filename,
        "file_url":file_url,
        "upload_date": datetime.utcnow(),
    }
    try:
        # Insert the document metadata into the 'documents' collection
        documents_result = app.db.documents.insert_one(doc_metadata)
        return str(documents_result.inserted_id)
    except Exception as e:
        print(f"An error occurred while inserting document metadata: {e}")
        return None
    
def find_documents():
    documents = app.db.documents.find({})
    return [serialize_doc(document) for document in documents]

def find_documents_by_username(username):
    documents = app.db.documents.find({"username_uploaded": username})
    return [serialize_doc(document) for document in documents]
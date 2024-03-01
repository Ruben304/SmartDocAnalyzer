from flask import current_app as app
from bson import ObjectId

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
        result = app.db.users.insert_one(user_data)  
        return result.inserted_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
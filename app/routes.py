from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from app.models import User, Document, Paragraph

users = {}
# POST = create
# GET = retrieve
# PUT = replace
# DELETE = delete
# PATCH = update

@app.route('/')
def home():
    return "Welcome to my Smart Doc Analyzer 1.0!"

# ====================================================== User Routes
# generate user list
@app.route("/users")
def user_list():
    users = User.query.order_by(User.username).all()
    users_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]

    return jsonify(users_data)

# create a user 
@app.route("/user/create", methods=["POST"])
def user_create():
    username = request.json.get("username")
    email = request.json.get("email")

    if username and email: # ensures input for all 
        user = User(username = username, email = email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"})
    else:
        return jsonify({"error": "Invalid method or missing data"}), 404   

# search for a user
@app.route("/user/<int:id>")
def user_detail(id):
    user = User.query.get_or_404(id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})

# edit a username 
@app.route("/user/<int:id>/edit", methods=["PUT"])
def edit_username(id):
    new_username = request.json.get("new_username")
    user = User.query.get_or_404(id)
    
    if user.username == new_username:
        return jsonify({"error": "Same username submitted"}), 400 
    
    
    if User.query.filter_by(username=new_username).first():
        return jsonify({"error": "Username already in use"}), 400
    
    user.username = new_username
    db.session.commit()
    return jsonify({"message": "Username edited successfully"})

# delete a user 
@app.route("/user/<int:id>/delete", methods=["DELETE"])
def user_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
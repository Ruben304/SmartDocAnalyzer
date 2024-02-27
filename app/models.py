from app import db 

# create custom objects for both projects and users 

# instances of users correspond to rows on a table
# user model 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # user id
    username = db.Column(db.String(128), unique=True, nullable=False) # username and ensures uniqueness
    email = db.Column(db.String)
    documents = db.relationship('Document', backref='user', lazy=True) # creates association of User and Documents, and lazy=True allows projects association to be lister

# similar to user
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True) # creates a column for ids, and marked as primary key to identify row
    title = db.Column(db.String(128), nullable=False) # creates a column for titles, stores up to 128 char and cant be empty
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # creates a column for user_id to link documents to users, and document must be associated with users
    paragraphs = db.relationship('Paragraph', backref='document', lazy=True) # creates association of Documents and Paragraph

class Paragraph(db.Model):
    id = db.Column(db.Integer, primary_key=True) # creates a column for ids, and marked as primary key to identify row
    name = db.Column(db.String(128), nullable=False) # creates a column for names, stores up to 128 char and cant be empty
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False) # creates a column for document id to linnk documents to paragraphs
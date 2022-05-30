from time import timezone
from . import db
# Module from flask that helps users login
from flask_login import UserMixin
from sqlalchemy.sql import func 

# Defining the schemea for the database layout. Just like EF core in C#

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # Whenever a new note is created, sqlalchemy func will time stamp with current time automatically when inserted
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Note must belong to a user. Setting relationship to user using foreign key
    # lowercase user is the name of the table in the database. One to many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
                                        # No user can have the same email as another user. 
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # Sets the relationship to the notes table by referencing the table name.
    # Foreign key lowercase, Referencing the table is Uppercase
    notes = db.relationship('Note')
    
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(120))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    year = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    read = db.Column(db.Boolean, default=False)
    shared = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_author = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    id_editorial = db.Column(db.Integer, db.ForeignKey('editorial.id'), nullable=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255))

class Editorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

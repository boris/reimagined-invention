from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(120))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    read = db.Column(db.Boolean, default=False)
    shared = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    isbn = db.Column(db.String(255))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_author = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    id_editorial = db.Column(db.Integer, db.ForeignKey('editorial.id'), nullable=False)
    id_genre = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

    author = db.relationship('Author', backref='books')
    editorial = db.relationship('Editorial', backref='books')
    genre = db.relationship('Genre', backref='books')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255))


class Editorial(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), primary_key=True)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), primary_key=True)

# many-to-many books/tags
tags = db.Table('books_tags',
                db.Column('id_tag', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('id_book', db.Integer, db.ForeignKey('book.id'), primary_key=True)
        )


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(255), nullable=False)

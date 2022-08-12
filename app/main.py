from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

from .models import User, Book
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():

    books_total = db.session.query(Book.id).filter(Book.id_user == current_user.id).count()
    books_read = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.read == True)).count()
    books_unread = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.read == False)).count()
    books_shared = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.shared == True)).count()

    return render_template('profile.html',
                           name = current_user.name,
                           email = current_user.email,
                           books_total = books_total,
                           books_read = books_read,
                           books_unread = books_unread,
                           books_shared = books_shared,
                           )

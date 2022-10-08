from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

from .models import User, Book, Author, Editorial, Genre
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add_book')
def add_book():
    if current_user.is_authenticated:
        return render_template('add_book.html',
                               greeting = current_user.name,
                               )
    else:
        return redirect(url_for('auth.login'))


@main.route('/add_book', methods = ['POST'])
def add_book_post():
    if current_user.is_authenticated:
        # Check author details and existence
        author_name = request.form.get("author_name")
        author_country = request.form.get("author_country")

        author_exists = Author.query.filter_by(name=author_name).first()

        if not author_exists:
            author = Author(country=author_country, name=author_name)
            db.session.add(author)
            db.session.commit()
            id_author = db.session.query(Author.id).filter(Author.name == author_name)

        id_author = db.session.query(Author.id).filter(Author.name == author_name)

        # Check editorial details and existence
        editorial_name = request.form.get("editorial_name")
        editorial_exists = Editorial.query.filter_by(name=editorial_name).first()

        if not editorial_exists:
            editorial = Editorial(name=editorial_name)
            db.session.add(editorial)
            db.session.commit()
            id_editorial = db.session.query(Editorial.id).filter(Editorial.name == editorial_name)

        id_editorial = db.session.query(Editorial.id).filter(Editorial.name == editorial_name)

        # Check genre existence
        genre_name = request.form.get("genre_name")
        genre_exists = Genre.query.filter_by(name=genre_name).first()

        if not genre_exists:
            genre = Genre(name=genre_name)
            db.session.add(genre)
            db.session.commit()
            id_genre = db.session.query(Genre.id).filter(Genre.name == genre_name)

        id_genre = db.session.query(Genre.id).filter(Genre.name == genre_name)

        # Add Book
        book_title = request.form.get('book_title')
        book_year = request.form.get('book_year')
        book_pages = request.form.get('book_pages')
        book_rating = request.form.get('book_rating')

        if request.form.get('book_is_read').lower() == 'si':
            is_read = True
        else:
            is_read = False

        if request.form.get('book_is_shared').lower() == 'si':
            is_shared = True
        else:
            is_shared = False

        book = Book(title = book_title,
                    year = book_year,
                    pages = book_pages,
                    read = is_read,
                    shared = is_shared,
                    rating = book_rating,
                    id_user = current_user.id,
                    id_author = id_author,
                    id_editorial = id_editorial,
                    id_genre = id_genre,
                    )
        db.session.add(book)
        db.session.commit()


        # Later this should redirect to 'main.book/book_id' or something like that
        return redirect(url_for('main.show_book', book_id = book.id))

    else:
        return redirect(url_for('auth.login'))


@main.route('/my_books')
def books():
    if current_user.is_authenticated:
        filtered_books = db.session.query(Book.id, Book.title, Book.rating, Book.id_author, Author.name.label('author_name'), Editorial.name.label('editorial_name'), Genre.name.label('genre_name'))\
            .join(Author)\
            .join(Editorial)\
            .join(Genre)\
            .filter((Book.id_author == Author.id) & (Book.id_editorial == Editorial.id) & (Book.id_user == current_user.id))\
            .order_by(Author.name.asc())

        return render_template('my_books.html',
                           greeting = current_user.name,
                           books = filtered_books,
                           )
    else:
        # Fix this route!!
        return redirect(url_for('main.login'))


@main.route('/profile')
def profile():
    if current_user.is_authenticated:
        books_total = db.session.query(Book.id).filter(Book.id_user == current_user.id).count()
        books_read = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.read == True)).count()
        books_unread = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.read == False)).count()
        books_shared = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.shared == True)).count()

        return render_template('profile.html',
                               name = current_user.name,
                               greeting = current_user.name,
                               books_total = books_total,
                               books_read = books_read,
                               books_unread = books_unread,
                               books_shared = books_shared,
                               )
    else:
        return redirect(url_for('auth.login'))


@main.route('/show_author/<int:author_id>')
def show_author(author_id):
    if current_user.is_authenticated:
        current_author = db.session.query(Author.name, Author.country).filter(Author.id == author_id)
        author_books = db.session.query(Book.id, Book.title, Book.year, Book.pages, Book.rating, Editorial.name.label('editorial_name'), Genre.name.label('genre_name'))\
            .filter(Book.id_author == author_id)\
            .join(Author)\
            .join(Editorial)\
            .join(Genre)

        return render_template('show_author.html',
                               greeting = current_user.name,
                               author = current_author,
                               books = author_books,
                               )


@main.route('/show_book/<int:book_id>')
def show_book(book_id):
    if current_user.is_authenticated:
        current_book = db.session.query(Book.title, Book.year, Book.pages, Book.read, Book.shared, Book.rating, Author.name.label('author_name'), Author.country.label('author_country'), Editorial.name.label('editorial_name'), Genre.name.label('genre_name'))\
            .filter(Book.id == book_id)\
            .join(Author)\
            .join(Editorial)\
            .join(Genre)

        return render_template('show_book.html',
                               greeting = current_user.name,
                               book = current_book,
                               )

    else:
        return redirect(url_for('main.login'))


@main.route('/test_utf8/')
def test_utf8():
    editorial_list = db.session.query(Editorial.name).filter(Editorial.id == 10).first()

    return str(editorial_list)

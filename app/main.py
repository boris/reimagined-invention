import random
import markdown
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc

# This is for debug
import traceback

from app.models import User, Book, Author, Editorial, Genre
from . import db
from .forms import BookForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add_book', methods = ['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()

    if form.is_submitted():
        # Check author details and existence
        author_name = request.form['author_name']
        author_country = request.form['author_country']

        author_exists = Author.query.filter_by(name=author_name).first()

        if not author_exists:
            author = Author(country=author_country, name=author_name)
            db.session.add(author)
            db.session.commit()
            id_author = db.session.query(Author.id).filter(Author.name == author_name)

        id_author = db.session.query(Author.id).filter(Author.name == author_name)

        # Check editorial details and existence
        editorial_name = request.form['editorial_name']
        editorial_exists = Editorial.query.filter_by(name=editorial_name).first()

        if not editorial_exists:
            editorial = Editorial(name=editorial_name)
            db.session.add(editorial)
            db.session.commit()
            id_editorial = db.session.query(Editorial.id).filter(Editorial.name == editorial_name)

        id_editorial = db.session.query(Editorial.id).filter(Editorial.name == editorial_name)

        # Check genre existence
        genre_name = request.form['book_genre']
        genre_exists = Genre.query.filter_by(name=genre_name).first()

        if not genre_exists:
            genre = Genre(name=genre_name)
            db.session.add(genre)
            db.session.commit()
            id_genre = db.session.query(Genre.id).filter(Genre.name == genre_name)

        id_genre = db.session.query(Genre.id).filter(Genre.name == genre_name)

        # Add Book
        book_title = request.form['book_title']
        book_year = request.form['book_year']
        book_pages = request.form['book_pages']
        book_rating = request.form['book_rating']
        book_review = request.form['book_review']
        book_isbn = request.form['book_isbn']

        # Normalize some values
        if request.form['book_is_read'].lower() == 'si':
            is_read = True
        else:
            is_read = False

        if request.form['book_is_shared'].lower() == 'si':
            is_shared = True
        else:
            is_shared = False

        if request.form['book_rating'] == '':
            book_rating = 0

        book = Book(title = book_title,
                    year = book_year,
                    pages = book_pages,
                    read = is_read,
                    shared = is_shared,
                    rating = book_rating,
                    review = book_review,
                    isbn = book_isbn,
                    id_user = current_user.id,
                    id_author = id_author,
                    id_editorial = id_editorial,
                    id_genre = id_genre,
                    )
        db.session.add(book)
        db.session.commit()


        # Later this should redirect to 'main.book/book_id' or something like that
        return redirect(url_for('main.show_book', book_id = book.id))

    return render_template('add_book.html',
                           greeting = current_user.name,
                           form = form,
                           )


@main.route('/delete_book/<int:book_id>', methods = ['GET', 'POST'])
@login_required
def delete_book(book_id):
    db.session.query(Book).filter(Book.id == book_id).delete()
    db.session.commit()

    return redirect(url_for('main.books'))


@main.route('/edit_book/<int:book_id>', methods = ['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(author_id=book.id_author, editorial_id=book.id_editorial, genre_id=book.id_genre)
    print(book.read, book.shared)

    form.book_is_read.data = 'Si' if book.read else 'No'
    form.book_is_shared.data = 'Si' if book.shared else 'No'

    if form.validate_on_submit():
        book.title = form.book_title.data
        book.author.name = form.author_name.data
        book.author.country = form.author_country.data
        book.pages = form.book_pages.data
        book.editorial.name = form.editorial_name.data
        book.year = form.book_year.data
        book.genre.name = form.book_genre.data
        book.read = form.book_is_read.data == 'Si'
        book.shared = form.book_is_shared.data == 'Si'
        book.rating = form.book_rating.data
        book.review = form.book_review.data
        book.isbn = form.book_isbn.data
        book.tags = form.book_tags.data

        db.session.commit()
        flash('El libro se ha actualizado exitosamente.', 'success')

        return redirect(url_for('main.show_book', book_id=book_id))

    return render_template('edit_book.html',
                           form=form,
                           book_id=book_id,
                           book=book,
                           greeting=current_user.name,
                           )


@main.route('/my_books')
@login_required
def books():
    filtered_books = db.session.query(Book.id, Book.title, Book.rating, Book.id_author, Book.id_genre, Book.id_editorial, Author.name.label('author_name'), Editorial.name.label('editorial_name'), Genre.name.label('genre_name'))\
        .join(Author)\
        .join(Editorial)\
        .join(Genre)\
        .filter((Book.id_author == Author.id) & (Book.id_editorial == Editorial.id) & (Book.id_user == current_user.id))\
        .order_by(Author.name.asc())

    return render_template('my_books.html',
                           greeting = current_user.name,
                           books = filtered_books,
                           )


@main.route('/profile')
@login_required
def profile():
    # Can the following come from the database?
    quotes = {
        "Vladimir Nabokov": {
            "Saber que tienes algo bueno para leer antes de irte a la cama es una de las sensaciones más agradables",
            "La lectura es una de las formas de la felicidad y debería ser accesible para todos",
        },
        "Lloyd Alexander": {
            "Sigue leyendo. Es una de las más maravillosas aventuras que cualquier persona puede tener"
        },
        "Benjamin Franklin": {
            "La lectura es para la mente lo que el ejercicio para el cuerpo",
            "La inversión en conocimiento paga el mejor interés"
        },
        "The black mamba": {
            "Dedication sees dreams come true",
            "May you always remember to enjoy the road, especially when it’s a hard one",
            "Hard work outweighs talent — every time.",
            "The most important thing is to try and inspire people so that they can be great in whatever they want to do.",
        },
        "Jorge Luis Borges": {
            "Que otros se enorgullezcan por lo que han escrito, yo me enorgullezco por lo que he leído",
            "La lectura es una conversación con los hombres más ilustres de los siglos pasados",
            "De los diversos instrumentos del hombre, el más asombroso es, sin duda, el libro. Los demás son extensiones de su cuerpo. El microscopio, el telescopio, son extensiones de su vista; el teléfono es extensión de la voz; luego tenemos el arado y la espada, extensiones del brazo. Pero el libro es otra cosa: el libro es una extensión de la memoria y la imaginación",
        },
        "Roberto Bolaño": {
            "La lectura es una forma de soledad, de aislamiento, de ruptura de la vida inmediata, mientras que al mismo tiempo es una apertura a un mundo diferente y quizás mejor",
            "La lectura es una amistad",
        },
        "Irene Vallejo": {
            "Toda biblioteca es un viaje; todo libro un pasaporte sin caducidad",
            "La lectura, como brújula, le abría los caminos de lo desconocido. En un mundo caótico, adquirir libros es un acto de equilibrio al filo del abismo",
            "Reunir todos los libros existentes es otra forma — simbólica, mental, pacífica — de poseer el mundo",
            "Los libros tiene voz y hablan salvando epocas y vidas. Las librerías son esos territorios mágicos donde, en un acto de inspiración, escuchamos los ecos suaves y chisporroteantes de la memoria desconocida",
        }
    }

    author = random.choice(list(quotes.keys()))
    quote = random.choice(list(quotes[author]))

    books_total = db.session.query(Book.id).filter(Book.id_user == current_user.id).count()
    books_read = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.read == True)).count()
    books_unread = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.read == False)).count()
    books_shared = db.session.query(Book.id).filter((Book.id_user == current_user.id) & (Book.shared == True)).count()

    # Queries for data analysis
    books_by_country_subquery = db.session.query(Book.id_author).filter(Book.id_user == current_user.id).subquery()
    books_by_country_query = db.session.query(Author.country, func.count()).\
                filter(Author.id.in_(books_by_country_subquery)).\
                group_by(Author.country).\
                order_by(func.count().desc()).\
                limit(5)
    books_by_country = [(row[0], row[1]) for row in books_by_country_query.all()]


    return render_template('profile.html',
                           author = author,
                           quote = quote,
                           name = current_user.name,
                           greeting = current_user.name,
                           books_total = books_total,
                           books_read = books_read,
                           books_unread = books_unread,
                           books_shared = books_shared,
                           books_by_country = books_by_country,
                           )


@main.route('/show_author/<int:author_id>')
@login_required
def show_author(author_id):
    current_author = db.session.query(Author.name, Author.country).filter(Author.id == author_id)
    author_books = db.session.query(Book.id, Book.title, Book.year, Book.pages, Book.rating, Book.id_editorial, Book.id_genre, Editorial.name.label('editorial_name'), Genre.name.label('genre_name'))\
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
@login_required
def show_book(book_id):
    current_book = db.session.query(Book.id, Book.title, Book.year, Book.pages, Book.read, Book.shared, Book.rating, Book.review, Book.isbn, Author.name.label('author_name'), Author.country.label('author_country'), Editorial.name.label('editorial_name'), Genre.name.label('genre_name'))\
        .filter(Book.id == book_id)\
        .join(Author)\
        .join(Editorial)\
        .join(Genre)

    review = db.session.query(Book.review).filter(Book.id == book_id)
    review = markdown.markdown(review[0][0])

    #rev = []
    #for r in review:
    #    r = dict(r)
    #    r['content'] = markdown.markdown(r['content'])
    #    rev.append(r)

    return render_template('show_book.html',
                           greeting = current_user.name,
                           review = review,
                           book = current_book,
                           )


@main.route('/show_country/<string:author_country>')
@login_required
def show_country(author_country):
    author_country = author_country.lower()
    authors = db.session.query(Author.id, Author.name)\
        .filter(Author.country == author_country)\
        .filter(Book.id_author == Author.id)\
        .filter(Book.id_user == current_user.id)\
        .join(Book)\
        .order_by(Author.name.asc())

    return render_template('show_country.html',
                           greeting = current_user.name,
                           author_country = author_country,
                           authors = authors,
                           )


@main.route('/show_editorial/<int:editorial_id>')
@login_required
def show_editorial(editorial_id):
    current_editorial = db.session.query(Editorial.name).filter(Editorial.id == editorial_id)
    editorial_books = db.session.query(Book.id, Book.title, Book.year, Book.pages, Book.rating, Book.id_author, Book.id_genre, Author.name.label('author_name'), Genre.name.label('genre_name'))\
        .filter(Book.id_editorial == editorial_id)\
        .join(Author)\
        .join(Editorial)\
        .join(Genre)

    return render_template('show_editorial.html',
                           greeting = current_user.name,
                           editorial = current_editorial,
                           books = editorial_books,
                           )


@main.route('/show_genre/<int:genre_id>')
@login_required
def show_genre(genre_id):
    current_genre = db.session.query(Genre.name).filter(Genre.id == genre_id)
    genre_books = db.session.query(Book.id, Book.title, Book.id_author, Book.rating, Book.id_editorial, Editorial.name.label('editorial_name'), Author.name.label('author_name'))\
        .filter(Book.id_genre == genre_id)\
        .join(Author)\
        .join(Editorial)\
        .join(Genre)

    return render_template('show_genre.html',
                           greeting = current_user.name,
                           genre = current_genre,
                           books = genre_books,
                           )


@main.route('/test/<int:book_id>', methods = ['GET', 'POST'])
@login_required
def test(book_id):
    book = db.session.query(Book.title).filter(Book.id == book_id)

    return render_template('test.html', book=book)

from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, RadioField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField)
from wtforms.validators import InputRequired, NumberRange, DataRequired, EqualTo

from .models import Book, Author, Editorial, Genre
from . import db

class BookForm(FlaskForm):
    def __init__(self, *args, author_id=None, editorial_id=None, genre_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id = author_id
        self.editorial_id = editorial_id
        self.genre_id = genre_id

    book_title = StringField('Título', validators=[InputRequired()])
    author_name = StringField('Autor', validators=[InputRequired()])
    author_country = StringField('País')
    editorial_name = StringField('Editorial')
    book_genre = StringField('Género')
    book_year = IntegerField('Año')
    book_pages = IntegerField('Número de páginas')
    book_is_read = RadioField('¿Leído?',
                              choices=['Si', 'No'],
                              validators=[InputRequired()])
    book_is_shared = RadioField('¿Prestado?',
                              choices=['Si', 'No'],
                              validators=[InputRequired()])
    book_rating = IntegerField('Puntuación', validators=[NumberRange(min=0, max=5)])
    book_review = TextAreaField('Reseña')
    book_tags = StringField('Tags')
    submit = SubmitField('Agregar')

    def populate_obj(self, obj):
        super().populate_obj(obj)
        obj.author_id = self.author_id
        obj.editorial_id = self.editorial_id
        obj.genre_id = self.genre_id


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class SignupForm(FlaskForm):
    name = StringField('Nombre', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirmPassword = PasswordField('Repetir Password', [EqualTo(password, message="Password no coincide")])
    submit = SubmitField('Submit')



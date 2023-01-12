from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, RadioField, PasswordField, SubmitField)
from wtforms.validators import InputRequired, NumberRange, DataRequired, EqualTo

class AddBookForm(FlaskForm):
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
    book_rating = IntegerField('Puntuación', validators=[NumberRange(min=1, max=5)])
    book_tags = StringField('Tags')
    submit = SubmitField('Agregar')


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class SignupForm(FlaskForm):
    name = StringField('Nombre', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirmPassword = PasswordField('Repetir Password', [EqualTo(password, message="Password no coincide")])
    submit = SubmitField('Submit')



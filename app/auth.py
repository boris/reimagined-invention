from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from .models import User
from . import db
from .forms import SignupForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST'])
def login_post():
    email = request.form.get('email')
    password_hash = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password_hash):
        flash('Usuario o contraseña inválidos')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.profile'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.is_submitted():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('El email ya está registrado')
            return redirect(url_for('auth.signup'))

        new_user = User(name=name,
                        email=email,
                        password_hash=generate_password_hash(password, method='sha256'),
                        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

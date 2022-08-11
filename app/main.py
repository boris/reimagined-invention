from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

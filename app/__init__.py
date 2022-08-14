import os
import yaml
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user


# Read config file
if path.exists('/local/config.yaml'):
    config_file = open('/local/config.yaml', 'r')
else:
    config_file = open('config.yaml', 'r')

config = yaml.load(config_file, Loader=yaml.FullLoader)


# App init
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=config['auth']['secret_key'],
    SQLALCHEMY_DATABASE_URI=config['db']['uri'],
)

# DB def and init
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)


# Import models
from .models import User


# Login manager
login_manager = LoginManager()
login_user.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# Blueprint import
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


if __name__ == '__main__':
    app.run()

import os
import yaml
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Read config file
if path.exists('/local/config.yaml'):
    config_file = open('/local/config.yaml', 'r')
else:
    config_file = open('config.yaml', 'r')

config = yaml.load(config_file, Loader=yaml.FullLoader)

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=config['auth']['secret_key'],
    SQLALCHEMY_DATABASE_URI=config['db']['uri'],
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.init_app(app)
from .models import User

# Load the instance config
#app.config.from_pyfile('config.py', silent=True)

# Simple page to say hello
@app.route('/hello')
def hello():
    return 'Hello world!'

if __name__ == '__main__':
    app.run()

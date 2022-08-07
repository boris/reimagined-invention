import os
import yaml
from os import path
from flask import Flask

# Read config file
if path.exists('/local/config.yaml'):
    config_file = open('/local/config.yaml', 'r')
else:
    config_file = open('config.yaml', 'r')
config = yaml.load(config_file, Loader=yaml.FullLoader)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config['auth']['secret_key'],
        DATABASE=config['db']['uri'],
    )

    # Load the instance config
    app.config.from_pyfile('config.py', silent=True)

    # Simple page to say hello
    @app.route('/hello')
    def hello():
        return 'Hello world!'

    return app

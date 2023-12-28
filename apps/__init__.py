import traceback
from flask import Flask
from importlib import import_module
import openai
import os
from flask_sqlalchemy import SQLAlchemy
from apps.config import Config

db = SQLAlchemy()


try:
    # openai.api_type = Config.OPENAI_API_TYPE
    openai.api_key = Config.OPENAI_API_KEY
    # openai.api_base = Config.OPENAI_RESOURCE_ENDPOINT
    # openai.api_version = Config.OPENAI_API_VERSION
    openai.engine = Config.OPENAI_GPT_ENGINE
except Exception as err:
    print(Exception, err)
    traceback.print_exc()

# os.environ["OPENAI_API_TYPE"] = Config.OPENAI_API_TYPE
# os.environ["OPENAI_API_VERSION"] = Config.OPENAI_API_VERSION
# os.environ["OPENAI_API_BASE"] = Config.OPENAI_RESOURCE_ENDPOINT
os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY

def register_blueprints(app):
    # List of module names
    module_names = [
        'home'
    ]
    # Add more blueprint modules as needed
    # Register each blueprint
    for module_name in module_names:
        module = import_module(f'apps.{module_name}.routes')
        app.register_blueprint(module.blueprint)


def configure_database(app):
    with app.app_context():
        try:
            db.create_all()
            print("\nTEST: Tables created successfully.")
        except Exception as e:
            print('Error initializing database', e)
            traceback.print_exc()


def create_app():
    app = Flask(__name__)
    
    app_config = app.config.from_object('apps.config.Config')

    db.init_app(app)
    # Register blueprints dynamically
    register_blueprints(app)
    configure_database(app)

    return app
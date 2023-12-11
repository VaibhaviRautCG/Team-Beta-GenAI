from flask import Flask
from importlib import import_module

def create_app():
    app = Flask(__name__)

    # Register blueprints dynamically
    register_blueprints(app)

    return app

def register_blueprints(app):
    # List of module names
    module_names = [
        'home',
        # Add more blueprint modules as needed
    ]

    # Register each blueprint
    for module_name in module_names:
        module = import_module(f'apps.{module_name}.routes')
        app.register_blueprint(module.blueprint, url_prefix=f'/{module_name}')
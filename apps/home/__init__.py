from flask import Blueprint

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    template_folder='templates',
    url_prefix=''
)

from apps.home import routes  # Import routes to register them with the blueprint
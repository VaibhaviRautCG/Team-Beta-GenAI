from flask import render_template

from apps.home import blueprint

@blueprint.route('/')
def index():
    return "Hello, Flask!"
    # return render_template('home/index.html')

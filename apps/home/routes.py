from flask import render_template

from apps.home import blueprint

@blueprint.route('/')
def index():
    return "Hello, Flask! This is the first dummy page."
    # return render_template('home/index.html')

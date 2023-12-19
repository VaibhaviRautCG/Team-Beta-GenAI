from flask_wtf import FlaskForm
from wtforms import TextAreaField

class ChatForm(FlaskForm):
    message = TextAreaField('Message')

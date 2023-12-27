from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ChatForm(FlaskForm):
    user_message = StringField('Your message:') #, validators=[DataRequired()])
    submit = SubmitField('Send')
    clear = SubmitField("Clear Button")
    
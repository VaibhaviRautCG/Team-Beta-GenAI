from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class ChatForm(FlaskForm):
    user_message = StringField('Your message:') #, validators=[DataRequired()])
    submit = SubmitField('Send')
    clear = SubmitField("Clear Button")
    image = FileField('Image Upload', id="image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'PNG'], 'Images only!')])

    
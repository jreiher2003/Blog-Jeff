from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
	username = TextField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember me.')


class MessageForm(Form):
	title = TextField('Title', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired(),Length(max=140)])
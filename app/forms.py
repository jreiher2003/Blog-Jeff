from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me.')
    submit = SubmitField("Sign In")


class MessageForm(Form):
    title = TextField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(),Length(max=140)])
    submit = SubmitField("Create Post")


class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('email', validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField("Sign Up")
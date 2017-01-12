import os

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_github import GitHub 


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
github = GitHub(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import views
from models import *

login_manager.login_view = "login"
login_manager.login_message = u'You need to login first!'
login_manager.login_message_category = 'info'


# loads users info from db and stores it in a session
@login_manager.user_loader 
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
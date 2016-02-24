import os

from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt 
from flask.ext.login import LoginManager 


app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
# print os.environ['APP_SETTINGS']
# print app.config['POSTS_PER_PAGE']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


from app import views
from models import *

login_manager.login_view = "login"
login_manager.login_message = u'You need to login to post'
login_manager.login_message_category = 'info'


# loads users info from db and stores it in a session
@login_manager.user_loader 
def load_user(user_id):
	return User.query.filter(User.id == int(user_id)).first()
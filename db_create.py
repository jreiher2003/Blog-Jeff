
from app import db
from app.models import BlogPost, User


# create the database and the db table
db.create_all()
db.session.add(User("admin", "ad@min.com", "admin"))

db.session.add(BlogPost("Good", "I\'m good.",1))
db.session.add(BlogPost("Well", "I\'m well.",1))
db.session.add(BlogPost("Excellent", "I\'m excellent.",1))
db.session.add(BlogPost("Okay a test title", "This is a postgres product code post.",1))


# commit the changes
db.session.commit()
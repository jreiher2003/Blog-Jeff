import datetime 

from app import db, bcrypt

from slugify import slugify



class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=datetime.datetime.now())
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship("BlogPost", backref="author")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<name> {}'.format(self.name)


class BlogPost(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created  = db.Column(db.DateTime,  default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
                                       onupdate=datetime.datetime.now())

    def __init__(self, title, description, author_id):
        self.title = title
        self.description = description
        self.author_id = author_id
        
    @property 
    def slug(self):
        return slugify(self.title)
    
    @property 
    def format_date(self):
        return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=self.date_created)

    @property 
    def format_time(self):
        return '{dt:%I:%M %p}'.format(dt=self.date_created)

    @property 
    def last_modified_date(self):
        return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=self.date_modified)

    @property 
    def last_modified_time(self):
        return '{dt:%I:%M %p}'.format(dt=self.date_modified)

    def __repr__(self):
        return '<title> {}'.format(self.title)
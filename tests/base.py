from flask.ext.testing import TestCase
from app import app, db
from app.models import User



class BaseTestCase(TestCase):
    """A base test case."""
 
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        one = User(name='Testname', email="test@test.com", password="password")
        db.session.add(one)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
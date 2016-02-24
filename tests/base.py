from flask.ext.testing import TestCase
from app import app, db



class BaseTestCase(TestCase):
    """A base test case."""
 
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        # db.session.add(Place(name='Testname'))
        
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
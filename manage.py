import os
import unittest
import coverage
from app import app,db

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand 
import logging


app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
server = Server(host="0.0.0.0", port=5095)
manager = Manager(app)
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()



if __name__ == '__main__':
    # cov()
    manager.run()
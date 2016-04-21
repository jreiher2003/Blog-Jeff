import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # UPLOADS_DEFAULT_DEST = "/static/tmp/"
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
    S3_BUCKET = os.environ["S3_BUCKET"]


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MAIL_SUPPRESS_SEND = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
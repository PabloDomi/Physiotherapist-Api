import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    )
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT')

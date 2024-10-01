import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    STATIC_FOLDER = 'health_app/static'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/name_of_the_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


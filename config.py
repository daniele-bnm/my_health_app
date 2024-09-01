import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    STATIC_FOLDER = 'health_app/static'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://dan:miaKeyLong@localhost/nextcartdb_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
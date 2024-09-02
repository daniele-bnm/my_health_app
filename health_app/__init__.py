from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)

    from health_app import routes, models

    return app
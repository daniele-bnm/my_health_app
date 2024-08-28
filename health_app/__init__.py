from flask import Flask

from health_app.models import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')

db.init_app(app)

from health_app import routes, models

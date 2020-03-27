from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config.DevelopementConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app, resources={r'/*': {'origins': '*'}})

from . import views

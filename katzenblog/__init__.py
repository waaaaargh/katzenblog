from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api

app = Flask(__name__)
app.config.from_pyfile('../katzenblog.cfg')
db = SQLAlchemy(app)
api = Api(app,
          prefix='/api/0/')

from katzenblog.model import *
from katzenblog.views import *
from katzenblog.api import *

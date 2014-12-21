from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../katzenblog.cfg')
db = SQLAlchemy(app)

from katzenblog.model import *
from katzenblog.views import *

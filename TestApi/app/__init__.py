from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app.routes import *
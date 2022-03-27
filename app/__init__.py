from flask import Flask,render_template, request
from .config import Config
# from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

# db = SQLAlchemy(app)


from app import views




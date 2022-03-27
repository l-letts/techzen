from flask import Flask,render_template, request
from flask_wtf.csrf import CSRFProtect
from app.config import Config
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine



app = Flask(__name__)
# app.config.from_object(Config)

ENV = 'dev'
if ENV == 'dev':
    app.debug =True
    app.config['SQLALCHEMY_DATABASE_URI'] = "http://localhost/phpmyadmin/db_structure.php?db=dev_techzen_db"

app.config['SECRET_KEY'] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD']= ''
# app.config['MYSQL_DB'] = 'dev_techzen_db'

# engine = create_engine('postgresql://root@localhost:3306/dev_techzen_db')
# mysql = MySQL(app)

db = SQLAlchemy(app)

app.config.from_object(__name__) 
from app import views




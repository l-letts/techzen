from app import app
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE dev_techzen_db")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
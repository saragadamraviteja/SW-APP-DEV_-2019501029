
import os

from flask import Flask, session
from sqlalchemy import create_engine
from flask import render_template,  request, session
from flask_session import Session
# from books import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

app1 = Flask(__name__)

db1 = SQLAlchemy()

class Book(db1.Model):
    __tablename__ = "book"
    isbn = db1.Column(db1.String, primary_key = True)
    title = db1.Column(db1.String, nullable = False)
    author = db1.Column(db1.String, nullable = False)
    year = db1.Column(db1.String, nullable = False)

    def __init__(self, isbn, title,author,year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

# Configure session to use filesystem
app1.config["SESSION_PERMANENT"] = False
app1.config["SESSION_TYPE"] = "filesystem"
Session(app1)

app1.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app1.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app1.app_context().push()

db1.init_app(app1)
db1.create_all()


def uploadcsv():
    csvfile = open("books.csv")
    reader = csv.reader(csvfile)
    for isbn,title,author,year in reader:
        b = Book(isbn = isbn,title = title,author = author, year = year)
        db1.session.add(b)
    db1.session.commit()

if __name__ == "__main__":
    uploadcsv()


import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template,  request, session
from flask_session import Session
from books import *
import csv

app1 = Flask(__name__)


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


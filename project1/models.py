from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "details"
    username = db.Column(db.String, primary_key = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.timestamp = datetime.now()

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)

    def __init__(self, isbn, title,author,year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

class Review(db.Model):
    __tablename__ = "review"
    username = db.Column(db.String, primary_key = True, nullable = False)
    isbn = db.Column(db.String, primary_key = True, nullable = False)
    rating = db.Column(db.Integer)
    review = db.Column(db.String, nullable = False)

    def __init__(self, username,isbn, rating,review):
        self.username = username
        self.isbn = isbn
        self.rating = rating
        self.review = review
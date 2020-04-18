from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
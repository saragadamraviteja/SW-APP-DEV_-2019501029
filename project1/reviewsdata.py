import os
from flask import Flask, session
from flask_session import Session
from flask import render_template,  request, session

app2 = Flask(__name__)

db2 = SQLAlchemy()

class Review(db2.Model):
    __tablename__ = "reviews"
    username = db2.Column(db2.String,primary_key =True,nullable = False)
    isbn = db2.Column(db2.String, primary_key = True,nullable= False)
    title = db2.Column(db2.String, nullable = False)
    author = db2.Column(db2.String, nullable = False)
    
    

    def __init__(self, username,isbn, title,author):
        self.username = username
        self.isbn = isbn
        self.title = title
        self.author = author



app2.config["SESSION_PERMANENT"] = False
app2.config["SESSION_TYPE"] = "filesystem"
Session(app2)

app2.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app2.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app2.app_context().push()

db2.init_app(app1)
db2.create_all()
import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template,  request, session
from flask_session import Session
from data import *

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/register", methods = ['GET','POST'])
def register():
    
    if (request.method=="POST"):
        data.query.all()
        name = request.form.get("name")
        print(name)
        pswd = request.form.get("Password")
        print(pswd)
        
        contact = request.form.get("ContactNumber")
        print(contact)
        regist = data(username=name,ContactNumber=contact)
        db.session.add(regist)
        db.session.commit()
        return render_template("register.html",name=name)

    return render_template("register.html") 




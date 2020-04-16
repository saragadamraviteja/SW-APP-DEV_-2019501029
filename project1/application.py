import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template,  request, session
from flask_session import Session

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/register", methods = ['GET','POST'])
def register():
    
    if (request.method=="POST"):
        name = request.form.get("name")
        pswd = request.form.get("Password")
        print(pswd)
        return render_template("login.html",name=name)

    return render_template("register.html")




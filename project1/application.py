import os

from flask import Flask, session
from flask_session import Session
from flask import render_template,  request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from datetime import datetime

app = Flask(__name__)

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


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()

db.init_app(app)
app.secret_key = "temp"

db.create_all()


# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return render_template("index.html",name=username)
    else:
        return render_template("register.html")

@app.route("/admin")
def admin():
    users = User.query.order_by("timestamp").all()
    return render_template("admin.html", users = users)
    

@app.route("/register", methods = ['GET','POST'])
def register():
    if (request.method=="POST"):
        # data.query.all()
        name = request.form.get("name")
        print(name)
        password = request.form.get("Password")
        print(password) 
        contact = request.form.get("ContactNumber")
        print(contact)
        regist = User(username=name, password=password)
        if User.query.get(name):
            return render_template("register.html",name1=name)
        db.session.add(regist)
        db.session.commit()
        return render_template("register.html",name=name)
    return render_template("register.html")

@app.route("/auth", methods=['GET','POST'])
def auth():
    if(request.method=="POST"):
        name = request.form.get("name")
        print(name)
        password = request.form.get("Password")
        print(password)
        obj = User.query.get(name)
        if obj is None:
            return render_template("register.html",message="User not yet registered")
        if (obj.username == name and obj.password == password):
            session['username'] = request.form.get("name")
            return render_template("login.html",name=name)

        if(obj.username != name or obj.password != password):
            return render_template("register.html",message="Invalid Credentials")
    return render_template("register.html",message="Invalid Credentials")

@app.route("/logout")
def logout():
    session.pop('username')
    return render_template("register.html")



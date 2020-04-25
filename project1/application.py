import os

from flask import Flask, session
from flask_session import Session
from flask import render_template,  request, session
from flask import url_for, session, flash, jsonify, make_response
from models import db, User, Book, Review
from getlogin import get_login_details
from search import getbooks
from review import review_present
from bookpage import getbook

from datetime import datetime
import csv
from datetime import datetime

app = Flask(__name__)
# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.secret_key = "temp"

# db.create_all()


# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return render_template("login.html",name=username)
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

        check = get_login_details(name,password)

        obj = User.query.get(name)

        if check==1:
            return render_template("register.html",message="User not yet registered, Please sign up first")
        elif check==0 :
            session['username'] = request.form.get("name")
            return render_template("login.html",name=name)

        else:
            return render_template("register.html",message="Invalid Credentials, please enter correct username and password")
    return render_template("register.html",message="Invalid Credentials")


@app.route('/review', methods =['GET','POST'])
def review():
    if request.method == 'POST':           
        rating = request.form.get('review_tags')
        review = request.form.get('review_value')
        name = session['username']
        temp = list(request.form.items())
        print(temp)
        # print(temp[2][0])
        if rating is None:
            detail = Book.query.filter(Book.isbn == temp[1][0]).all()
            isbn = temp[1][0]
        else:
            detail = Book.query.filter(Book.isbn == temp[2][0]).all()
            isbn = temp[2][0]
        total_reviews = db.session.query(Review).filter(Review.isbn == isbn)
        # if rating is None:
        #     return render_template('bookpage.html',message = 'Please rate this book',sel_book = detail,total_reviews=total_reviews,isbn = isbn)
        flag = review_present(name,isbn)
        if flag:
            data = Review(username = name, isbn = isbn, rating = rating, review = review) 
            db.session.add(data)
            db.session.commit()
        else:
            return render_template('bookpage.html',message = 'You have already given review',sel_book = detail,total_reviews=total_reviews,isbn = isbn)
    return render_template('bookpage.html',name = session['username'], message1 = 'Review submitted succesfully.',total_reviews=total_reviews,sel_book = detail,isbn = isbn)


@app.route("/logout")
def logout():
    session.pop('username')
    return render_template("register.html")


def uploadcsv():
    csvfile = open("books.csv")
    reader = csv.reader(csvfile)
    for isbn,title,author,year in reader:
        b = Book(isbn = isbn,title = title,author = author, year = year)
        db.session.add(b)
    db.session.commit()

if __name__ == "__main__":
    uploadcsv()
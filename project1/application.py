import os

from flask import Flask, session
from flask_session import Session
from flask import render_template,  request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

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

class Book(db.Model):
    __tablename__ = "book"
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)

    def __init__(self, isbn, title,author,year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year


# class Review(db.Model):
#     __tablename__ = "review"
#     username = db.Column(db.String, primary_key = True, nullable = False)
#     isbn = db.Column(db.String, Primary_key=True,nullable = False)
#     review = db.Column(db.String, nullable = False)
#     rating = db.Column(db.String, nullable = False)

#     def __init__(self, username, isbn, review,rating ):
#         self.username = username
#         self.isbn = isbn
#         self.review = review
#         self.rating = rating

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

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_type = request.form.get('book_tags').lower()
        print(search_type)
        book_info = request.form.get('search_value').lower()
        print(book_info)
        book_info = f'%{book_info.lower()}%'
        books_result = Book.query.order_by(Book.title.asc()).filter(getattr(Book, search_type).ilike(book_info)).all()
        print(books_result)
        if not books_result:
            return render_template('login.html', message="No books found.")
        return render_template('login.html', books_result=books_result)
    return render_template('login.html')



@app.route('/book/<string:isbn_id>')
def isbn(isbn_id):
        print(isbn_id)
        sel_book = Book.query.filter(Book.isbn == isbn_id).all()
        # book=sel_book[0]
        print(len(sel_book))
        # for i in sel_book:
        #     title = i.title
        #     author = i.author
        #     isbn = i.isbn
        #     year = i.year
        #     name = session['username']
        # print(name,author,title,isbn,year)
        return render_template('bookpage.html',book = sel_book[0])





@app.route("/logout")
def logout():
    session.pop('username')
    return render_template("register.html")


# @app.route("/review", methods = ['GET', 'POST'])
# def review():
#     if request.method == 'POST':
#         rating = request.form.get('rating').lower()
#         review = request.form.get('review_value')
#         # regist = User(username=name, password=password)

        


def uploadcsv():
    csvfile = open("books.csv")
    reader = csv.reader(csvfile)
    for isbn,title,author,year in reader:
        b = Book(isbn = isbn,title = title,author = author, year = year)
        db.session.add(b)
    db.session.commit()

if __name__ == "__main__":
    uploadcsv()
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
            return render_template("test.html",name=name)

        else:
            return render_template("register.html",message="Invalid Credentials, please enter correct username and password")
    return render_template("register.html",message="Invalid Credentials")

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_type = request.form.get('book_tags').lower()
        print(search_type)
        book_info = request.form.get('search_value').lower()
        print(book_info)
        book_info = f'%{book_info.lower()}%'

        books_result = getbooks(search_type,book_info)

        # books_result = Book.query.order_by(Book.title.asc()).filter(getattr(Book, search_type).ilike(book_info)).all()
        # print(len(books_result))
        books_found = len(books_result)
        print(books_found)
        if not books_result:
            return render_template('login.html', message="No books found.", name = session['username'])
        return render_template('login.html', books_result=books_result, name = session['username'], message = "Total "+str(books_found)+" results found.")
    return render_template('login.html', name = session['username'])

@app.route("/test")
def test():
    name = session['username']
    return render_template("test.html",name = name)

@app.route("/api/search",methods = ["POST"])
def apisearch():
    searchType = request.form.get("type").lower()
    print(searchType)
    userinput = request.form.get("query").lower()
    print(userinput)
    userinput = f'%{userinput.lower()}%'
    allBooks = getbooks(searchType, userinput)
    # print(allBooks)
    # allBooks_json = [{"isbn":'0380795272',"title":'Krondor: The Betrayal',"author":'Raymond E. Feist'}]
    allBooks_json = [] 

    for book in allBooks:
        eachBook = {}
        eachBook["isbn"] = book.isbn
        eachBook["title"] = book.title
        eachBook["author"] = book.author
        allBooks_json.append(eachBook)
    return jsonify({"allBooks":allBooks_json})


@app.route("/api/bookpage",methods = ["POST"])
def apibookpage():
    isbn = request.form.get("isbn")
    bookreturned = getbook(isbn) 
    # print(bookreturned[0],"tets")
    Bookdetails = {}
    Bookdetails["isbn"] = bookreturned[0].isbn
    Bookdetails["title"] = bookreturned[0].title
    Bookdetails["author"] = bookreturned[0].author
    Bookdetails["year"] = bookreturned[0].year
    return jsonify({"bookinfo":Bookdetails})

@app.route("/api/review",methods = ["POST"])
def apibookpagereview():
   isbn = request.form.get("isbn")
   total_reviews = db.session.query(Review).filter(Review.isbn == isbn)
   print('ravi')
   print(total_reviews)
   print(len(list(total_reviews)))
   tot_reviews = {}
   for i in total_reviews:
       tot_reviews[i.username] = [i.review,i.rating] 
   print(tot_reviews)
   return jsonify({'total_review': tot_reviews})

@app.route("/api/submit-review", methods = ["POST"])
def submitReview():
    rating = request.form.get('rating')
    review = request.form.get('review')
    isbn = request.form.get('isbn')
    name = session['username']
    print(name)
    r = Review.query.filter_by(username = name, isbn = isbn).first()
    # flag = review_present(name,isbn)
    print(r)
    if r is None:
        data = Review(username = name, isbn = isbn, rating = rating, review = review)
        db.session.add(data)
        db.session.commit()
        # return jsonify({'flag1': 'true'})
        return jsonify({"name" : [True,name]})
    return jsonify({'name': [False,name]})



@app.route('/book/<string:isbn_id>')
def isbn(isbn_id):
    book = getbook(isbn_id)
    # sel_book = Book.query.filter(Book.isbn == isbn_id).all()
    total_reviews = db.session.query(Review).filter(Review.isbn == isbn_id)
    return render_template('bookpage.html',sel_book =book,total_reviews = total_reviews,isbn= isbn_id, name = session['username'])

@app.route('/review', methods =['GET','POST'])
def review():
    if request.method == 'POST':           
        rating = request.form.get('review_tags')
        review = request.form.get('review_value')
        name = session['username']
        print(name)
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
            print(data)
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
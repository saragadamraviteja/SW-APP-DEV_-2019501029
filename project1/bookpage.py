from models import Book


def getbook(isbn):
    book1 = Book.query.filter(Book.isbn == isbn).all()
    return book1

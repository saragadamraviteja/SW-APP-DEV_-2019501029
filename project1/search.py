from models import Book

def getbooks(search_type,book_info):
    books= Book.query.order_by(Book.title.asc()).filter(getattr(Book, search_type).ilike(book_info)).all()
    return books
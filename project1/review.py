from models import Review

def review_present(name,isbn):
    if (Review.query.filter_by(username = name, isbn = isbn).first() == None):
        return False
    else: return True

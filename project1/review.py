from models import Review

def review_present(name,isbn):
    print('nnan',name)
    if (Review.query.filter_by(username = name, isbn = isbn).first() == None):
        return True
    else: return False

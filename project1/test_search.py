import unittest
from Testhelp import Testhelp
from search import getbooks
from models import Book


class Test_search(Testhelp):

    def test_valid(self):
        books_result = getbooks('title','Mein kampf')
        print(books_result)
        if not books_result:
            flag = False
        else: flag = True 
        print(flag)
        self.assertTrue(flag)
    
    def test_invalid(self):
        books_result = getbooks('isbn','the')
        if not books_result:
            flag = False
        else: flag = True 
        self.assertFalse(flag)

    def test_not_present(self):
        books_result = getbooks('author','abhiram')
        if not books_result:
            flag = False
        else: flag = True 
        self.assertFalse(flag)
    
if __name__ == "__main__":
       unittest.main()         
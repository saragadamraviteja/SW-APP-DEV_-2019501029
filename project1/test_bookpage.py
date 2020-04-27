import unittest
from Testhelp import Testhelp
from bookpage import getbook
from models import Book


class Test_bookpage(Testhelp):

    def test_valid(self):
        book = getbook('081299289X')
        self.assertEqual(book.title,'China Dolls')
    
    def test_invalid(self):
        book = getbook('0345498127')
        self.assertEqual(book.author,'David Nicholls')

    def test_valid2(self):
        book = getbook('0061053716')
        self.assertEqual(book.year,'1991')

if __name__ == "__main__":
       unittest.main() 
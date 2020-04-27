import unittest
from Testhelp import Testhelp
from bookpage import *


class Test_bookpage(Testhelp):

    def test_valid(self):
        book = getbook('081299289X')
        self.assertEqual(book.title,'China Dolls')
    
    def test_invalid(self):
        book = getbook('034')
        if (book.author!='David Nicholls'):
            flag = False
        self.assertFalse(flag)

    def test_valid2(self):
        book = getbook('0061053716')
        self.assertEqual(book.year,'1991')

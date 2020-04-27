import unittest
from Testhelp import Testhelp
from review import review_present
from models import Review


class Test_review(Testhelp):

    def test_valid(self):
        flag = review_present('rrr','0553262149')
        self.assertTrue(flag)
    
    def test_invalid(self):
        flag = review_present('rrr','0553262140')
        self.assertFalse(flag)

    def test_valid2(self):
        flag = review_present('siva','0375701230')
        self.assertTrue(flag)

if __name__ == "__main__":
       unittest.main() 
    
        
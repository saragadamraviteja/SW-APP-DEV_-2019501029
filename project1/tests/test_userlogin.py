import unittest
from Testhelp import Testhelp
from getlogin import get_login_details
from models import User

class Test_getlogin(unittest.TestCase):

    def test_valid(self):
        flag = get_login_details('rrr','5678')
        self.assertEqual(flag,0)
    
    def test_invalid(self):
        flag = get_login_details('rrr','123')
        self.assertEqual(flag,-1)

    def test_not_present(self):
        flag = get_login_details('bhuvanbam','124')
        self.assertEqual(flag,1)
    
if __name__ == "__main__":
       unittest.main()    
import unittest
import os
from flask import Flask,request, render_template,redirect
from flask import url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from init_config import initialize_testing_app
# from flask import Flask,request,render_template


class Testhelp(unittest.TestCase):

    def setUp(self):
        self.app = initialize_testing_app()
        # app = Flask(__name__)
        # db = SQLAlchemy()

        # if not os.getenv("DATABASE_URL"):
        #     raise RuntimeError("DATABASE_URL is not set")

        # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        # db.init_app(app)
        # app.app_context().push()
    def test_touppercase(self):
        self.assertEquals("foo".capitalize(),"Foo")
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()




from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class data(db.Model):
    __tablename__ = "profile"
    username = db.Column(db.String, nullable =False)
    ContactNumber = db.Column(db.Integer, primary_key=True)
    


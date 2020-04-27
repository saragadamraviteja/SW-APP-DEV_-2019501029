from datetime import datetime
from models import User

# class User(db.Model):
#     __tablename__ = "details"
#     username = db.Column(db.String, primary_key = True, nullable = False)
#     password = db.Column(db.String, nullable = False)
#     timestamp = db.Column(db.DateTime, nullable = False)

#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.timestamp = datetime.now()

def get_login_details(name,password):
    obj = User.query.get(name)
    
    if obj is None:
        return 1
    elif (obj.username == name and obj.password == password):
        return 0
    else: return -1




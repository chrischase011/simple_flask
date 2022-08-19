from datetime import datetime
from email.policy import default
from sqlite3 import Timestamp
from time import timezone
from app import db, login_manager
from flask_login import UserMixin

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, default=0)
    name = db.Column(db.String(100), nullable = False)
    power = db.Column(db.String(100), nullable = False)
    weapon = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(500), default="")

    def __init__(self, name, power, weapon, description):
        self.name = name
        self.power = power 
        self.weapon = weapon
        self.description = description
    
    def __repr__(self):
        return "<Characters %r>" % self.id

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    full_name = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.Integer, default=int(0))
    token = db.Column(db.Text, nullable=True)
    email_verified = db.Column(db.Integer, default=int(0))
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, email, full_name, password, token):
        self.email = email
        self.full_name = full_name
        self.password = password
        self.token = token
    
    def __repr__(self):
        return "<Users %r>" % self.id

db.create_all()
db.session.commit()

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


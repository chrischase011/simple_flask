from app import db, login_manager
from flask_login import UserMixin

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key = True)
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

    def __init__(self, email, full_name, password):
        self.email = email
        self.full_name = full_name
        self.password = password
    
    def __repr__(self):
        return "<Users %r>" % self.id

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


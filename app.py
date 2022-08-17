# @app

# lib
from unicodedata import name
from flask import Flask, render_template, session, abort, request, url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# OS
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='assets',
            template_folder='templates')
app.config["SECRET_KEY"] = os.urandom(32)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chase_website.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

db = SQLAlchemy(app)

db.create_all()
db.session.commit()

# Blueprint
from flask import Blueprint
from controller import controller
from auth import auth

# Register blueprint
app.register_blueprint(controller, name="controller")
app.register_blueprint(auth, name="auth")




if __name__ == "__main__":
    app.run(debug=True)
# @app
# lib
from unicodedata import name
from flask import Flask, render_template, session, abort, request, url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
# OS
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='assets',
            template_folder='templates')

app.config.from_pyfile('config.py')
app.config["SECRET_KEY"] = os.urandom(32)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Mail
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

db = SQLAlchemy(app)

migrate = Migrate(app, db)



# Blueprint
from flask import Blueprint
from controller import controller
from auth import auth

# Register blueprint
app.register_blueprint(controller, name="controller")
app.register_blueprint(auth, name="auth")

if __name__ == "__main__":
    app.run()
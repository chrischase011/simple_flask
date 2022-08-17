from app import render_template
from flask import Blueprint

controller = Blueprint('controller', __name__)

@controller.route('/test')
def test():
    return 'Test'

@controller.route('/')
@controller.route('/home')
def home():
    return render_template("pages/index.html")

@controller.route('/profile')
def profile():
    return render_template("pages/profile.html",  title="Profile")

@controller.route('/game')
def game():
    return render_template("pages/game.html", title="Game")

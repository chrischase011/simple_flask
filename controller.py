# @Blueprint/controller

#lib
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

@controller.route('/blog')
def blog():
    return render_template("pages/blog.html",  title="blog")

@controller.route('/game')
def game():
    return render_template("pages/game.html", title="Game")

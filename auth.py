# @Blueprint/auth

#lib
from app import db
from flask import render_template, session, abort, request, url_for,redirect,flash
from flask_login import login_user, current_user, login_required, logout_user
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from models import Characters, Users
auth = Blueprint('controller', __name__)


# AUTH
@auth.route('/login', methods= ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('controller.home'))
    form = LoginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(email=request.form['email']).first()

        if not user or not check_password_hash(user.password, request.form['password']):
            flash("Invalid email or password", 'error')
        else :
            login_user(user)
            return redirect(url_for('controller.home'))
    
    return render_template('auth/login.html', title="Login", form=form)

@auth.route('/register', methods=["GET", "POST"])
def register():
    form = Register()
    if request.method == 'POST':

        if form.validate_on_submit():
            user = Users.query.filter_by(email = request.form['email']).first()
            if user :
                flash("Email address already exists. Please choose different email.")
            else:
                result = Users(request.form['email'], request.form['full_name'], generate_password_hash(request.form['password'], method='sha256'))
                db.session.add(result)
                db.session.commit()
                flash("You can now login.", 'success')
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title="Register", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('controller.home'))


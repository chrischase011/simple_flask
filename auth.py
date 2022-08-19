# @Blueprint/auth

#lib
from urllib import response
from app import db,mail, os
from flask import render_template, session, abort, request, url_for,redirect,flash
from flask_login import login_user, current_user, login_required, logout_user
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from flask_mail import Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from base64 import b64encode
import random, string
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
                token = token_generator()
                check_token = Users.query.filter_by(token = token).first()

                while check_token:
                    token = token_generator()
                    check_token = Users.query.filter_by(token = token).first()

                result = Users(request.form['email'], request.form['full_name'], generate_password_hash(request.form['password'], method='sha256'), token = token)
                db.session.add(result)
                db.session.commit()

                # msg = Message("Chase's Flask Website", recipients=[request.form['email']])
                
                # msg.html = render_template("auth/email/token.html", name=request.form['full_name'], token=token)
                # mail.send(msg)

                to_emails = [
                    To(email=request.form['email'],
                    name=request.form['full_name'],
                    dynamic_template_data={
                        "name" : request.form['full_name'],
                        "url" : url_for('auth.verify', token=token, _external=True)
                    },subject="Email Verification")
                ]

                message = Mail(from_email=os.environ.get('MAIL_DEFAULT_SENDER'),
                    to_emails=to_emails,
                    subject="Email Verification")
                message.template_id = "d-8beaaee54d7c4cfdad51b8e5a2429b3f"

                try:
                    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sendgrid_client.send(message)
                except Exception as e:
                    print(e.message)

                flash("You can now login.", 'success')
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title="Register", form=form)

@auth.route('/verify/<token>', methods=["GET"])
def verify(token):
    check_token = Users.query.filter_by(token = token).first()
    
    if not check_token:
        flash("Invalid link. Please check your email for the link.", 'error')
        return redirect(url_for('controller.home'))

    return render_template("auth/verify.html", token=token)

@auth.route('/biz')
def biz():
    return render_template("auth/email/token.html", name="Test", token="oiqerewoiruweirwerewrwer")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('controller.home'))



def token_generator(length = 40, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))
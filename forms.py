from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

class Register(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    full_name = StringField("Full Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8), EqualTo("confirm_password", "Password don't match")])
    confirm_password = PasswordField("Confirm Password", validators=[Length(min=8)])
    register = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")
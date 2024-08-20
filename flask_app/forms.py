
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_app.models import User, Post


######################################################################################
################################# Regsteration Form ##################################
######################################################################################

class RegisterationFormn(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email =  StringField("Email",
                         validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError("This Username has already been taken! Please choose another username!")

    def validate_username(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError("This Email has already been taken! Please choose another email!")

######################################################################################
################################# Login Form #########################################
######################################################################################
       
class LoginForm(FlaskForm):
    email =  StringField("Email",
                         validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


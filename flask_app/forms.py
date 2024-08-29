
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_app.models import User, Post
from flask_login import current_user


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

######################################################################################
################################# Update Account Form ################################
######################################################################################

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email =  StringField("Email",
                         validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture",
                         validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError("This Username has already been taken! Please choose another username!")
        

    def validate_username(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError("This Email has already been taken! Please choose another email!")

######################################################################################
################################# Post Form ##########################################
######################################################################################

class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
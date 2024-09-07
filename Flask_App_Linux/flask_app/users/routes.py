import os
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask_app import db, bcrypt
from flask_app.models import Post, User
from flask_app.users.forms import RegisterationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_app.users.utils import save_picture, send_reset_email


#creating an instance of Blueprint module
users = Blueprint("users", __name__)

############################################################################################
############################### Registeration page #########################################
############################################################################################

@users.route("/register", methods= ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created! Please procced to login!', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title= "Register", form=form)

############################################################################################
############################### Login page #################################################
############################################################################################

@users.route("/login", methods = ['GET', 'POST'])
def login():
    #if the current user is authenticated then we are redirecting it to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #args is a dictionary
            #redirect to the next page if the next parameter is present else redirect to the home page.
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f"Login unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title= "Login", form=form)

############################################################################################
############################### Logout Button ##############################################
############################################################################################

@users.route("/logout")
def logout():
    logout_user() #using the function from the flask_login module to logout all the users and clears the remember cookies as well.
    return redirect(url_for('main.home'))

############################################################################################
############################### Account Details ############################################
############################################################################################


#################### Routes for Account info ######################################

@users.route("/account", methods = ['GET', 'POST'])
@login_required #this decorator is used to notify that for accounts route to be accessed we need to login first.
#If you decorate a view with this, it will ensure that the current user is logged in and authenticated before calling the actual view. 
# (If they are not, it calls the LoginManager.unauthorized callback.)
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #Removing the previously used picture from storage before saving new
            prev_picture = os.path.join(users.root_path, 'static/profile_pics', current_user.image_file)
            if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
                os.remove(prev_picture)

            #use save_picture function to get the picture name and save the resized image in the picture path.
            picture_name = save_picture(form.picture.data)
            current_user.image_file = picture_name
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account details have been updated successfully", "success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET': #this by defalt populates the current user details in the form.
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title= "Account", image_file= image_file, form= form)




############################################################################################
##################################### Post Owner ###########################################
############################################################################################

@users.route("/user/<string:username>") 
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username= username).first_or_404()
    posts = Post.query\
        .filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) 
    return render_template("user_posts.html", posts=posts, user=user)


############################################################################################
##################################### Reset Password #######################################
############################################################################################


#--------------------------------------------------------------------------------------------------
#reset request is a route to place a reset request using the email id when we click forgot password

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #user should be logged out to raise a reset request
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user= user)
        flash("An email has been sent to reset the password! Please check your Inbox !!", "info")
        return redirect(url_for('users.login'))
    
    return render_template("reset_request.html", form= form, title= "Reset Password")

#--------------------------------------------------------------------------------------------------
#reset password is a route to change the password by clicking the link recieved in the email id.
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #user should be logged out to reset the password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token=token)
    if user is None:
        flash("This is an invalid/ expired token", "warning")
        return redirect(url_for('users.reset_request'))
    
    form =  ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! Please procced to login!', 'success')
        return redirect(url_for('users.login'))
    
    return render_template("reset_token.html", form= form, title= "Reset Password")

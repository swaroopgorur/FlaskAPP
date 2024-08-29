############################### Import  ####################################################

from flask import render_template, url_for, flash, redirect, request, abort
from flask_app.forms import RegisterationFormn, LoginForm, UpdateAccountForm, PostForm
from flask_app.models import User, Post
from flask_app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image

############################################################################################
############################### Global Variable Declaration ################################
############################################################################################

# posts = [
#     {
#         'author': 'Swaroop.GS',
#         'title': 'Lies of Narendra Modi',
#         'content': 'Modi has a “purana rishta” - an old relationship – with lies and untruths and that bears no repetition. Indian news television, or whatever passes off for it, is beyond redemption. It is rotting at the bottom of a bottomless pit. What needs to be underscored is the coverage in India’s English language newspapers. Two of them had Modi’s astonishing claim on their front page: The Times of India and the Indian Express. And both did perfect stenography. They simply narrated what Modi had said, without attempting even a semblance of a fact-check, the basic function of any journalist. ‘If I do Hindu-Muslim, won’t be fit for public life: PM Modi’, said the TOI headline and the story provided no context or background for readers to judge his claim. ‘The day I do Hindu-Muslim, I will be unworthy of public life… I will not do it, it’s my resolve: PM Modi,’ said the Express headline. Though its story reproduced quotes from his April 21 Banswara speech, it failed to point out the obvious: that the PM was making an obvious misrepresentation of his remarks.Modi’s speech at Banswara is crystal clear in its words and language. It is not a dog whistle, it an open and loud howl for human consumption that is recorded on video. Given the undeniable nature of his remarks, Modi’s disingenuous claim did not merit a stenographic report. It needed to be reported as a fact check, so that readers and viewers could be armed with the necessary health warnings. [See here and here]. The India Cable is a newsletter so was even more direct: We told our readers yesterday that Modi had lied.',
#         'date_posted': 'August 08, 2024'
#     },
#     {
#         'author': 'Supriya.J',
#         'title': 'Facts of Nirmala Sitharaman',
#         'content': 'First of all, let’s understand who will decide whether Nirmala Sitharaman is a good finance minister or not. And what are the criteria to judge her performance? Ideally in the office, your Boss will do your appraisal or competency evaluation. He will decide whether you are good or not. So the onus and authority of judging Nirmala Sitharaman as the Finance Minister are with Modi Ji. Modi Ji must have been pleased with her performance as the Defense Minister in his first term, so he has given her the all-important Finance Ministry. During the Rafale deal controversy, Madam Sitharaman fought valiantly in Modi’s favor. Modi Ji must have been very highly impressed with her fighting spirit and loyalty. So it seems Madam Sitharaman has duly earned her position in the new cabinet. As such it’s Modi Ji and only Modi Ji going to evaluate her as the Finance Minister.',
#         'date_posted': 'August 07, 2024'
#     }
# ]

############################################################################################
############################### Home page ##################################################
############################################################################################

@app.route("/")
@app.route("/home") #route is a decorator that is used to handle all the backend stuff and retun the o/p of the called function
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5) 
    return render_template("home.html", posts=posts)

############################################################################################
############################### About page #################################################
############################################################################################

@app.route("/about") #route is a decorator that is used to handle all the backend stuff and retun the o/p of the called function
def about():
    return render_template('about.html', title='About') 

############################################################################################
############################### Registeration page #########################################
############################################################################################

@app.route("/register", methods= ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterationFormn()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created! Please procced to login!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title= "Register", form=form)

############################################################################################
############################### Login page #################################################
############################################################################################

@app.route("/login", methods = ['GET', 'POST'])
def login():
    #if the current user is authenticated then we are redirecting it to the home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #args is a dictionary
            #redirect to the next page if the next parameter is present else redirect to the home page.
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Login unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title= "Login", form=form)

############################################################################################
############################### Logout Button ##############################################
############################################################################################

@app.route("/logout")
def logout():
    logout_user() #using the function from the flask_login module to logout all the users and clears the remember cookies as well.
    return redirect(url_for('home'))

############################################################################################
############################### Account Details ############################################
############################################################################################

#################### Saving the picture by renaming the fn #######################

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + extension
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    ############## Resizing the Image using Pillow ###############
    output_size = (125,125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn

#################### Routes for Account info ######################################

@app.route("/account", methods = ['GET', 'POST'])
@login_required #this decorator is used to notify that for accounts route to be accessed we need to login first.
#If you decorate a view with this, it will ensure that the current user is logged in and authenticated before calling the actual view. 
# (If they are not, it calls the LoginManager.unauthorized callback.)
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #Removing the previously used picture from storage before saving new
            prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
            if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
                os.remove(prev_picture)

            #use save_picture function to get the picture name and save the resized image in the picture path.
            picture_name = save_picture(form.picture.data)
            current_user.image_file = picture_name
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account details have been updated successfully", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET': #this by defalt populates the current user details in the form.
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title= "Account", image_file= image_file, form= form)

############################################################################################
########################## Create, Fetch, Update and Delete Posts ##########################
############################################################################################

#this route is used to create new posts
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        author = current_user
        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.commit()
        flash("You post has been created successfully!", "success")
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

#this route is used to fetch the posts if exists else throw an error
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts.html", title=post.title, post=post)

#this route is used to update the posts
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been updated successfully!", "success")
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content 
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

#this route is used to delete the post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been deleted successfully!!", "success")
    return redirect(url_for("home"))

############################################################################################
##################################### Post Owner ###########################################
############################################################################################

@app.route("/user/<string:username>") 
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username= username).first_or_404()
    posts = Post.query\
        .filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) 
    return render_template("user_posts.html", posts=posts, user=user)
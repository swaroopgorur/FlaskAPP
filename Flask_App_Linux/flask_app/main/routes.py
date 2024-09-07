from flask import Blueprint, render_template, request
from flask_app.models import Post

main = Blueprint("main", __name__)

############################################################################################
############################### Home page ##################################################
############################################################################################

@main.route("/")
@main.route("/home") #route is a decorator that is used to handle all the backend stuff and retun the o/p of the called function
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5) 
    return render_template("home.html", posts=posts)

############################################################################################
############################### About page #################################################
############################################################################################

@main.route("/about") #route is a decorator that is used to handle all the backend stuff and retun the o/p of the called function
def about():
    return render_template('about.html', title='About') 
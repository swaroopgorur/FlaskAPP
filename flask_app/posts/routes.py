from flask import Blueprint, render_template, abort, flash, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask_app import db
from flask_app.models import Post
from flask_app.posts.forms import PostForm


posts = Blueprint("posts", __name__)

############################################################################################
########################## Create, Fetch, Update and Delete Posts ##########################
############################################################################################

#this route is used to create new posts
@posts.route("/post/new", methods=['GET', 'POST'])
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
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts.html", title=post.title, post=post)


#this route is used to update the posts
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content 
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

#this route is used to delete the post
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been deleted successfully!!", "success")
    return redirect(url_for('main.home'))



from flask_app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

######################################################################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


############################### Database Classes - Model Instances ###################################

#each class is a table in Database which is an instance of db.Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable= False)
    email = db.Column(db.String(120), unique=True, nullable= False)
    image_file = db.Column(db.String(20), nullable= False, default= 'default.jpg')
    password = db.Column(db.String(60), nullable=True)
    #users will author posts and hence it is " one to many relationship "
    #as one user can author many posts but a post can have only one author, here posts attr has a relationship to the Post class(model)....
    posts = db.relationship('Post', backref='author', lazy=True)
    #backref -> adding a column called author to the post model, we can use the author attr to get the user who created the post
 
    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable= False, default= datetime.utcnow)
    content = db.Column(db.Text, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #above we are using user.id and not User.id because the tables created are by default in small letters.

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
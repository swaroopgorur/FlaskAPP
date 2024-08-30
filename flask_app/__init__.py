from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_app.config import Config



#############################################################################################
###################################### Extensions ###########################################
#############################################################################################

#Extensions are not included inside the create_app function because extensions can be used for 
# many apps.

############################### Creating Instances  #########################################

db = SQLAlchemy() #SQLAlchemy db instance
bcrypt = Bcrypt() #to generate password hash
login_manager =  LoginManager() #instance of LoginManager import from flask_login
login_manager.login_view = 'users.login' #we need to tell the function where the login view is created.login is function name of the route
login_manager.login_message_category = 'info' #just adding some bootstrap class to show the messages in a better way.
mail = Mail()

#############################################################################################
################################ Create APP function  #######################################
#############################################################################################

def create_app(config_class = Config):

    ############################### Flask App Creation #################################
    app = Flask(__name__) #__name__ holds the name of the module
    app.config.from_object(Config)

    ################### Intitializing Extension obj ####################################
    # init_app: Initialize a Flask application for use with this extension instance. 
    # This must be called before accessing the database engine or session with the app.
    db.init_app(app=app)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)
    mail.init_app(app=app)

    ####### Importing Blueprint instances from Routes and Registering Blueprint ########
    from flask_app.users.routes import users
    from flask_app.posts.routes import posts
    from flask_app.main.routes import main
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


############################### Flask App Creation #########################################

app = Flask(__name__) #__name__ holds the name of the module

#-------------------------------------------------------------------------------------------
#created using the secrets module
#secrets.token_hex(16) ---> 'b4b1b3011043cf50e962c2c2dab8ac2c'
app.config['SECRET_KEY'] = 'b4b1b3011043cf50e962c2c2dab8ac2c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#-------------------------------------------------------------------------------------------

db = SQLAlchemy(app) #SQLAlchemy db instance
bcrypt = Bcrypt(app) #to generate password hash
login_manager =  LoginManager(app) #instance of LoginManager import from flask_login
login_manager.login_view = 'login' #we need to tell the function where the login view is created.lgin is function name of the route
login_manager.login_message_category = 'info' #just adding some bootstrap class to show the messages in a better way.
#-------------------------------------------------------------------------------------------
from flask_app import routes

#-------------------------------------------------------------------------------------------
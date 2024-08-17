from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


############################### Flask App Creation #########################################

app = Flask(__name__) #__name__ holds the name of the module

#-------------------------------------------------------------------------------------------
#created using the secrets module
#secrets.token_hex(16) ---> 'b4b1b3011043cf50e962c2c2dab8ac2c'
app.config['SECRET_KEY'] = 'b4b1b3011043cf50e962c2c2dab8ac2c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#-------------------------------------------------------------------------------------------

db = SQLAlchemy(app) #SQLAlchemy db instance
bcrypt = Bcrypt(app) 
#-------------------------------------------------------------------------------------------
from flask_app import routes

#-------------------------------------------------------------------------------------------
Use the below command to install all the required packages:
pip install -r requirements.txt

#---------------------------------------------------------------------------------
Run the below command to start the flask application:
==>  python flask_app.py

#---------------------------------------------------------------------------------
To initialize the database and
    add the data to the database
        query data from the database
            follow the below steps:
==> import os
==> os.system('cls' if os.name == 'nt' else 'clear') ==> clear the data

==> open python in the same path as of the project 
==> from flask_app import app, db
==> db.create_all() ==> creates an instance of site.db inside the project 
==> from flask_app import User, Post
==> user1 = User(a='',b= '',c= '')
==> user2 = User(a='',b= '',c= '')
==> with app.app_context():
==>     db.session.add(user1)
==>     db.session.add(user2)
==>     db.session.commit()
==>     User.query.all() ==> returns a list of all the user elements that are present
==>     User.query.first() ==> returns the first user elements 
==>     User.query.filter_by(attr = 'param').all() ==> data returned as a list
==>     User.query.filter_by(attr = 'param').first() ==> data not returned as a list
==>     user = User.query.filter_by(attr = 'param').first()
==>     db.drop_all() ==> delete all the table and their data

#---------------------------------------------------------------------------------
forms.py:
==> Contains the code for the registeration form and login forms

#---------------------------------------------------------------------------------
base.html:
------> Basic layut structure for all the html pages.
------> Needs to be extended in all the html pages

home.html:
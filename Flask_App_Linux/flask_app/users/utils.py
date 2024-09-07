import os, secrets
from PIL import Image
from flask_app import mail
from flask import current_app
from flask import url_for
from flask_mail import Message


#################### Saving the picture by renaming the fn #######################

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + extension
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

    ############## Resizing the Image using Pillow ###############
    output_size = (125,125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn


#################### Function to send reset password link #######################

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender='noreply@demo.com',  # Set the sender to a 'noreply' address
        recipients=[user.email]
    )
    msg.body = f''' To reset your password, please click on the below link \n
{url_for('users.reset_token', token= token, _external= True)} 

If you didnot request for a password reset, you can simply ignore this email!!  
'''
    mail.send(msg)
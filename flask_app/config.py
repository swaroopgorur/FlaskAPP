import os

class Config:
    #created using the secrets module
    #secrets.token_hex(16) ---> 'b4b1b3011043cf50e962c2c2dab8ac2c'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')
    PERSPECTIVE_API_KEY = os.environ.get('PERSPECTIVE_API_KEY')

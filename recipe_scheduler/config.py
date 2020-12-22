"""
Setting for SQL server
"""

import os


class Config:
    """
    Setting for SQL and mail server
    """
    # .bash-profile
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abc123ced456'
    WTF_CSRF_SECRET_KEY = os.getenv('SECRET_KEY') or 'abc123ced456'
    # os.environ.get('DATABASE_URL') for Heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              os.environ.get('DATABASE_URL')

    # # for google email
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # # To use Heroku, please "heroku config set" for following 2 parameters
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
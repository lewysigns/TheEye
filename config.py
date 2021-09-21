import os 
from dotenv import load_dotenv
load_dotenv()


#
# The .env file contains all of the configuration parameters
#
# NOTE: This file will need to be created by the user to run the application. 
#       It should be placed at the same directory level as app.py
#       The syntax should look as follows:
#               DATABASE_URI = "<Your_database_uri_here>"
#

class Config:
    """
    Base configuration class. Contains default configuration settings
    """

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='party time')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.getenv('CELERY_URL ')
    RESULT_BACKEND = os.getenv('RESULT_BACKEND')

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
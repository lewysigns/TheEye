#
# Environment Libraries
#
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
import os

#
# Local Libraries
#
#from taskmanager import celery
from taskmanager import celery
from resources.event import Event
from db import db
from resources.event import Event



#
# The .env file contains all of the configuration parameters
#
# NOTE: This file will need to be created by the user to run the application. 
#       It should be placed at the same directory level as app.py
#       The syntax should look as follows:
#               DATABASE_URI = "<Your_database_uri_here>"
#

load_dotenv()
database_uri   = os.environ["DATABASE_URI"]
celery_url     = os.environ["CELERY_URL"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['CELERY_BROKER_URL'] = celery_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Deprecated configuration, need to set to false to avoid warning.
api    = Api(app)
celery.config_from_object(app)

@app.before_first_request
def create_tables():
    db.create_all()

#
# Adding all the resources an application can use to interface with the database
#
api.add_resource(Event,'/event/') # Get/Post an event

if __name__ == '__main__':
    
    db.init_app(app)
    app.run(port=5000, debug=True)


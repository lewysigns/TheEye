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
from config import Config
from resources.event import Event
from db import db


def create_app():

    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.Config')
    app.config.from_object(CONFIG_TYPE)

    # Configure celery
    celery.conf.update(app.config)  

    api    = Api(app)

    #
    # Adding all the resources an application can use to interface with the database
    #
    api.add_resource(Event,'/event/') # Get/Post an event

    return app
    
if __name__ == '__main__':
    
    app = create_app()

    @app.before_first_request
    def create_tables():
        db.create_all()
        
    db.init_app(app)
    app.run(port=5000, debug=True)


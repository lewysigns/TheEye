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
from resources.event import Event,EventSession,EventCategory,EventTimerange


#
# The .env file contains all of the configuration parameters
#
# NOTE: This file will need to be created by the user to run the application. 
#       It should be placed at the same directory level as app.py
#       The syntax should look as follows:
#               DATABASE_URI = "<Your_database_uri_here>"
#

load_dotenv()
database_uri = os.environ["DATABASE_URI"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Deprecated configuration, need to set to false to avoid warning.
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Event,'/event/')
api.add_resource(EventSession,'/event/session/<string:session_id>')
api.add_resource(EventCategory,'/event/category/<string:category>')
api.add_resource(EventTimerange,'/event/timerange/')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
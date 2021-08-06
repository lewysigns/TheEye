from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
import os


#
# The .env file contains all of the configuration parameters
#
load_dotenv()
database_uri = os.environ["DATABASE_URI"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Deprecated configuration, need to set to false to avoid warning.
api = Api(app)



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
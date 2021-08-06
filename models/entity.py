from db import db
from sqlalchemy.dialects.postgresql import JSON


class EntityModel(db.Model):
    __tablename__ = 'entities'

    id         = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(80))
    category   = db.Column(db.String(80))
    name       = db.Column(db.String(80))
    data       = db.Column(JSON)
    timestamp  = db.Column(db.DateTime)

    def __init__(self,session_id,category,name,data,timestamp):
        """Constructor"""

        self.session_id = session_id,
        self.category   = category
        self.name       = name
        self.data       = data
        self.timestamp  = timestamp

    def json(self):
        """ Function to return json of class data"""
        return {'session_di': self.session_id,
                'category':self.category,
                'name':self.name,
                'data':self.data,
                'timestamp':self.timestamp
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
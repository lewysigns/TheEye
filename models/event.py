from db import db
from sqlalchemy.dialects.postgresql import JSON


class EventModel(db.Model):
    __tablename__ = 'events'

    id         = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(80))
    category   = db.Column(db.String(80))
    name       = db.Column(db.String(80))
    data       = db.Column(JSON)
    timestamp  = db.Column(db.DateTime())

    def __init__(self,session_id,category,name,data,timestamp):
        """Constructor"""

        self.session_id = session_id,
        self.category   = category
        self.name       = name
        self.data       = data
        self.timestamp  = timestamp

    def json(self):
        """ Function to return json of class data"""
        return {'session_id': self.session_id,
                'category':self.category,
                'name':self.name,
                'data':self.data,
                'timestamp':self.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
        }

    @classmethod
    def find_by_session_id(cls, session_id):
        return {'events': list(
                map(
                    lambda x: x.json(), 
                    cls.filter_by(session_id=session_id)
                    )
                )
            }

    @classmethod
    def find_by_category(cls, category):
        return {'events': list(
                map(
                    lambda x: x.json(), 
                    cls.query.filter_by(category=category)
                    )
                )
            }

    @classmethod
    def find_by_time_range(cls, init_time, end_time):
        return  {'events': list(
                map(
                    lambda x: x.json(), 
                    cls.query.filter(and_(timestamp >= init_time,timestamp <= end_time))
                    )
                )
            }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
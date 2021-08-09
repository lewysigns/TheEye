from db import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import and_
from taskmanager import celery
import redis


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
        return {'events': [x.json() for x in 
                    cls.query.filter_by(session_id=session_id).order_by(EventModel.timestamp)]
            }

    @classmethod
    def find_by_category(cls, category):
        return {'events': [x.json() for x in 
                    cls.query.filter_by(category=category).order_by(EventModel.timestamp) ]
            }

    @classmethod
    def find_by_time_range(cls, init_time, end_time):
        return  {'events': [x.json() for x in 
                    cls.query.filter(and_(EventModel.timestamp >= init_time,
                    EventModel.timestamp <= end_time)).order_by(EventModel.timestamp)]
            }              
    @celery.task(bind=True)        
    def save_to_db(self):

        #
        # Placing a unqiue lock , that can only be owned
        # by a single worker at a time to prevent race conditions
        #

        have_lock = False
        save_lock = redis.Redis().lock("my_key")
        try:
            have_lock = my_lock.acquire(blocking=False)
            if have_lock:
                db.session.add(self)
                db.session.commit()
        finally:
            if have_lock:
                my_lock.release()



    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
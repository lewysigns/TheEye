from flask_restful import Resource, reqparse
import datetime


from models.event import EventModel

class Event(Resource):
    #
    # Required arguements devilivered in a payload , when a post request
    # is made
    #
    parser = reqparse.RequestParser()
    parser.add_argument('session_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="Every event needs a category"
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Every event needs a name"
                        )
    parser.add_argument('data',
                        type=dict,
                        required=True,
                        help="Every event need data"
                        ) 
    parser.add_argument('timestamp',
                        type=str,
                        required=True,
                        help="Every event needs a timestamp"
                        )                                                                              

    def post(self):

        data = Event.parser.parse_args()

        event = EventModel(**data)

        try:
            event.save_to_db.delay()
        except:
            return {"message": "An error occurred inserting the event."}, 500

        return {"message": "Event has been Saved!"}, 201


class EventSession(Resource):

    def get(self,session_id):
        """ Request all events with a given session_id"""

        events = EventModel.find_by_session_id(session_id)
        if events:
            return events
        return {'message': 'event not found with that session id'}, 404


class EventCategory(Resource):

    def get(self,category):
        """ Request all events with a given category"""

        events = EventModel.find_by_category(category)
        if events:
            return events
        return {'message': 'event not found in that category'}, 404 

class EventTimerange(Resource):
    #
    # Required arguements devilivered in a payload , when a post request
    # is made
    #
    parser = reqparse.RequestParser()
    parser.add_argument('init_time',
                        type=str,
                        required=True,
                        help="""There needs to be a begining time for 
                                requesting events within a certain timerange"""
                        ) 
    parser.add_argument('end_time',
                        type=str,
                        required=True,
                        help="""There needs to be an end time for 
                                requesting events within a certain timerange"""
                        ) 
    def get(self):
        """ Reqeuest all events with a given time range"""
        data = EventTimerange.parser.parse_args()
        
        #
        # Converting Data String times to timestamps
        #
        init_time = datetime.datetime.strptime(data["init_time"], "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S.%f")
        
        events = EventModel.find_by_time_range(init_time,end_time)
        if events:
            return events
        return {'message': 'event not found in that time range'}, 404  

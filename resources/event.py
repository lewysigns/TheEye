from flask_restful import Resource, reqparse


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
            event.save_to_db()
        except:
            return {"message": "An error occurred inserting the event."}, 500

        return event.json(), 201


class EventSession(Resource):

    def get_session(self,session_id):
        """ Request all events with a given session_id"""

        events = eventModel.find_by_session_id(session_id)
        if events:
            return events
        return {'message': 'event not found with that session id'}, 404


class EventCategory(Resource):

    def get_category(self,category):
        """ Request all events with a given category"""

        events = eventModel.find_by_category(category)
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
    def get_time_range(self):
        """ Reqeuest all events with a given time range"""
        data = event.parser.parse_args()
        "2021-01-01 09:15:27.243860"
        init_time = datetime.datetime.strptime(data["init_time"], "%Y-%m-%d %H:%M:%S.%f").timestamp()

        events = eventModel.find_by_time_range(init_time,end_time)
        if events:
            return events
        return {'message': 'event not found in that time range'}, 404  

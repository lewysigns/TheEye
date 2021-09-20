from flask_restful import Resource, reqparse
from flask import request
import datetime
from taskmanager import celery
from models.event import EventModel

class Event(Resource):
    #
    # Required arguements devilivered in a payload , when a post request
    # is made
    #
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('session_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    post_parser.add_argument('category',
                        type=str,
                        required=True,
                        help="Every event needs a category"
                        )
    post_parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Every event needs a name"
                        )
    post_parser.add_argument('data',
                        type=dict,
                        required=True,
                        help="Every event need data"
                        ) 
    post_parser.add_argument('timestamp',
                        type=str,
                        required=True,
                        help="Every event needs a timestamp"
                        )    

    #
    # Required arguements devilivered in a payload , when a time request
    # is made
    #
    time_parser = reqparse.RequestParser()
    time_parser.add_argument('init_time',
                        type=str,
                        required=True,
                        help="""There needs to be a begining time for 
                                requesting events within a certain timerange"""
                        ) 
    time_parser.add_argument('end_time',
                        type=str,
                        required=True,
                        help="""There needs to be an end time for 
                                requesting events within a certain timerange"""
                        )   

    def parse_time_range(self):
        """ parse time range payload for query """
        data = Event.time_parser.parse_args()

        #
        # Converting Data String times to timestamps
        #
        init_time = datetime.datetime.strptime(data["init_time"], "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S.%f")
        
        return (init_time,end_time)

    def process_filter(self,):
        """ Process Query parameter to set appropriate filter """
        filter_args = request.args.get('filter',None)
        print(filter_args)
        filter_params = filter_args.split(',')
        print(filter_params)
        filter = filter_params[0]
        if len(filter_params) > 1:
            filter_arg = filter_params[1]
            return (filter,filter_arg)

        return (filter,None)

    @celery.task(bind=True)    
    def get(self):
        """ Get request with multiple query options"""

        #
        # process filters
        #
        (filter,filter_arg) = self.process_filter()
        
        #
        # if statement tree
        #

        if filter == "session_id":
            print(filter_arg)
            events = EventModel.find_by_session_id(filter_arg)
        elif filter == "category":
            events = EventModel.find_by_category(filter_arg)
        elif filter == "time":
            (init_time,end_time) = self.parse_time_range()
            events = EventModel.find_by_time_range(init_time,end_time)
        else:
            return {'message': f'requested filter, {filter}, currenlty not supported'},400

        if events:
            return events
        return {'message': 'event not found with that criteria'}, 404

    def post(self):

        data = Event.post_parser.parse_args()

        event = EventModel(**data)

        try:
            event.save_to_db()
        except:
            return {"message": "An error occurred inserting the event."}, 500

        return {"message": "Event has been Saved!"}, 201

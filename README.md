# Coding Challenge: The Eye

---

## Problem Statement

---

1. Create a service that will collect and store event data from web application interactions.
2. Create the request to access the data.

## Operational Functionality

---

* Receive ***event(s)*** sent by a single, or multiple, application(s)
* Check the message came form a *trusted-client*
* Set up validation for each event type
* Group events by session, ordered by time of occurance

### Events

Events are a payload of json format that contain the following information

    - session  id : A key identifying what session of the application sent the event
    - category : Some Category identifying the type of event
    - name : the name of the application sending the event
    - data : a payload of data is unique to the category
    - timestamp : timestamp of when the event was sent


example:

```
{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "party",
  "name": "AppName",
  "data": {
    "host": "www.party.com",
    "path": "/"
  },
  "timestamp": "2021-09-26 09:15:27.243860"
}
```


## Requirements

---

* Allow threading to process events in the background
* Send responses to received events
* avoid race conditions
* written in python
* ligth effort (3-4 hours)

## Querys/Records

---

* querys
    + session
    + category
    + time range

* errors
    + unexpected value in payload
    + invalid time stamps

## Extra Credit

---

* Documentation
* Dockerize
* reusable client

### Assumptions

---

1. Because the applications are "trusted-clients", I do not have to add authentication
2. Applications are associated to sessions in some other application
3. The entire event is not passed through the url, e.i /<name>/<category>/
4. Time-Zone is consistent because no zone is given in the time-stamp
5. There was a trailing comma by mistake in the first example event message. The comma
    after the <"path": "/"***,***>
6. Time Range Get Request will come with a payload defining the initial and end times

### Required Libraries

---

See requirements.txt for a list of all the libraries used to run this application.

You can run the following command to install all the requirements into a local environment:

    pip install -r requirements.txt

## How to run the app

---

First you need to start your server:

    redis-server

Then you need to start your celery workers:

    Celery --app celery_worker.celery worker --pool=solo --loglevel=info --logfile=celery.log

Finally you can run your application:

    python app.py

Now you're ready to go!

## Conclusions

---

This git repository has a flask api that can receive events and store them appropriately in a database. The application responds with each event, both if a failure occurs or upon success. Background task are handled using celery workers on a redis server. The background task chosen were posting an event ot the database and getting events from the database. All api calls were tested using postman.

Thank you for the experience!

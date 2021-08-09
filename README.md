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

* flask
* flask_restful
* flask_sqlalchemy
* dotenv
* sqlalchemy
* psycopg2

## Conclusions

---

This git repsotory has a flask api that can receive events and store them appropriately in a database. The application responds with each event, both if a failure occurs or upon success. There was an attempt to process multiple events in the background using celery, but I kept running into issues and decided the time spent was getting to long to resolve. I believe it is something minor that I would be able to resolve with a team to bounce errors off of. Because of this, I was not able to test the race condition logic in place as well. Both of these can be found in the *background* branch of the repository.

Thank you for the experience!
# Coding Challenge: The Eye

---

## Problem Statement

---

1. Create a service that will collect and store event data from web application interactions.
2. Create the request to access the data.

## Operational Functionality

---

* Receive ***event(s)*** sent by a single, or multiple, application(s)
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

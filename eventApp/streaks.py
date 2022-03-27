"""
Code By Michael Dorado
Date: 3/26/22

This little script right here is to implement a portion of the streaks system on the front end.
We are going to take in a dictionary object (from the DB) with info pertaining to user login times.
From that info we can compile a list of all the mindfulness events that happened in a time frame.
We then update the last login to the current time. Which we save to the DB.
We then pass a list of events off to the front end.
"""

import datetime
from eventApp.models import Events, Streaks
from eventApp.serializers import EventsSerializer, StreaksSerializer

from django import views


def streakEvents(userData):
    #Debugging Text
    print("User Data: ", userData)

    #Set the current time to right now
    currentTime = datetime.datetime.now().replace(microsecond=0)
    print("Current Time: ", currentTime)

    #Get the last login time from userdata and turn the string into datetime format
    LastLogin = datetime.datetime.strptime(userData['LastLogin'], '%Y-%m-%dT%H:%M:%SZ')
    #This commented out line is for testing and debug to reset the last login time 1/2
    #LastLogin = datetime.datetime(2022, 3, 20, 00,30,00,00)
    print("Last Login:", LastLogin)

    #Get all calendar objects that have the Mindfulness Tag from DB and serialize them 
    calendar = Events.objects.filter(UserEmail=userData['UserEmail'], EventType=2)
    calendar_serializer = EventsSerializer(calendar, many=True)

    #Get the eligible dates
    eligible_dates = []
    for event in calendar_serializer.data:
        #Turn the start date of an event into a datetime var (was a str)
        start_date = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ')
        #If the event start was before the current time and after the last login, add the date to the list
        if start_date > LastLogin and  start_date <= currentTime:
            eligible_dates.append(event)
    print("Eligible Dates:",eligible_dates)

    #Get the user data
    old_userData = Streaks.objects.get(UserEmail = userData['UserEmail'])
    #Update the user data to have the last login be "now"
    userData['LastLogin'] = currentTime
    #This commented out line is for testing and debug to reset the last login time 2/2
    #userData['LastLogin'] = LastLogin

    #Save the new last login time
    user_streaks_serializer = StreaksSerializer(old_userData, data=userData)
    if(user_streaks_serializer.is_valid()):
        user_streaks_serializer.save()

    #return the eligible dates that we found
    return eligible_dates


    
    


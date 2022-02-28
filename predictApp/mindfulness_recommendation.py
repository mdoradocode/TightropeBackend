"""

    This file will use the mindfulness event data selected by the user on sign up and scan through the calendar to find an open time that we believe is a good time to practice mindfulness.

    Layout in my mind:
        1. retrieve a given users event data for next week (needs to be sent from the database, Icould cut it off here but it would waste computing power)
        2. order data by date/event 
        3. scan to find open times where time between events is greater than a time hyperparameter
        4. select the soonest time window that fits the time hyperparameter
        5. consider 
        
    NOTES: 
    This is completely contingent upon how the calendar and event_preferences are sent into this program.

    It also assumes that there are no overlapping events
        As part of this, all day events like birthdays will need to be stored separately and not fed into this program.

    Once we implement this, I will troubleshoot this again and make sure it is all working properly for normal use.

    There are probably edge cases, a reader can think of any of these, please send me a discord message.

    I also am not sure if I'm working with datetime correctly, it was a recommendation from the internet.

    This was built by Cooper Flourens

"""

import datetime
import calendar
import random

from eventApp.models import UserPreferences

# Hyperparameters

#   this is the id of start_time in the calendar
START_TIME_ID = 'StartDate'

# id of end_time in an event
END_TIME_ID = 'EndDate'

# threshold for event recommendations
TIME_THRESHOLD = datetime.timedelta(hours=1)

#   length of leisure event id
PREFERRED_EVENT_LENGTH = "UserPreferenceDuration"



def mindfulness_recommendation_finder(calendar, event_preferences):
    #   Get only events this week
    today = datetime.datetime.today()
    max = datetime.datetime.today()+datetime.timedelta(days=7)

    #   get the eligible dates
    eligible_dates = []
    for event in calendar:
        start_date = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ')
        if start_date > today and start_date < max:
            eligible_dates.append(event)
    
    #   sort the events by date
    sorted_dates = sorted(eligible_dates, key=lambda x: x["StartDate"])

    #   shuffle the event preferences for fun haha
    random.shuffle(event_preferences)

    #   setting up variables for consistency
    time_for_event = 0
    previous_event = None
    count = 0
    for event in sorted_dates:
        # don't do this for the first event
        if count != 0:
            #   if the time between the previous event and the current event is greater than the time threshold
            start_time = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ')
            end_time = datetime.datetime.strptime(previous_event["EndDate"], '%Y-%m-%dT%H:%M:%SZ')
            if (start_time - end_time) > TIME_THRESHOLD:
                #   then we have a good time to practice mindfulness
                time_for_event = end_time + datetime.timedelta(minutes=15) # add 15 minute buffer after previous event
                length_of_event = (start_time - datetime.timedelta(minutes=15)) - end_time # subtract 15 minutes before next event
                #   check if any preferred events fit the time window
                for preferred_event in event_preferences:
                    preferred_event_length = datetime.timedelta(minutes=preferred_event[PREFERRED_EVENT_LENGTH])
                    if preferred_event_length < length_of_event:
                        #   if so, return the event, and recommend the time
                        recommended_event = {
                            "UserEmail": event["UserEmail"],
                            "EventName": preferred_event["UserPreference"],
                            "StartDate": time_for_event,
                            "EndDate": time_for_event + datetime.timedelta(minutes=preferred_event[PREFERRED_EVENT_LENGTH]),
                            "Location": "",
                            "EventType": 0,
                            "StressLevel": 0,
                            "Notes": preferred_event["UserPreferenceNotes"]
                        }
                        return recommended_event
        previous_event = event
        count+=1
    return None
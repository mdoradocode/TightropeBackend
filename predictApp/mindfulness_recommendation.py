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

# Hyperparameters

#   this is the id of start_time in the calendar
START_TIME_ID = 'startTime'

# id of end_time in an event
END_TIME_ID = 'endTime'

# threshold for event recommendations
TIME_THRESHOLD = datetime.timedelta(hours=1)

#   length of leisure event id
PREFERRED_EVENT_LENGTH = "length"



def mindfulness_recommendation_finder(calendar, event_preferences):

    #   only keep events that are in the next week
    calendar = {key: value for key, value in calendar.items() if value.start_time.date() <= datetime.datetime.now().date() + datetime.timedelta(days=7)}

    #   sort the events by start time
    dict(sorted(calendar.items(), key=lambda item: item[START_TIME_ID]))

    # compare end time of previous event to the start time of next event to find a good open time
    time_for_event = 0
    previous_event = None
    count = 0
    for event in calendar:
        # don't do this for the first event
        if count != 0:
            #   if the time between the previous event and the current event is greater than the time threshold
            if (event[START_TIME_ID] - previous_event[END_TIME_ID]) > TIME_THRESHOLD:
                #   then we have a good time to practice mindfulness
                time_for_event = previous_event[END_TIME_ID] + datetime.timedelta(minutes=15) # add 15 minute buffer after previous event
                length_of_event = time_for_event - (event[START_TIME_ID] - datetime.timedelta(minutes=15)) # subtract 15 minutes before next event
                #   check if any preferred events fit the time window
                for preferred_event in event_preferences:
                    if preferred_event[PREFERRED_EVENT_LENGTH] < length_of_event:
                        #   if so, return the event, and recommend the time
                        return preferred_event, time_for_event
                        #   note, we may want to package this information into an event object and return that as a calendar event, where:
                            #   event.name = preferred_event["name"]
                            #   event.start_time = time_for_event
                            #   event.end_time = time_for_event + preferred_event["length"]
                            #   event.location = preferred_event["location"]
                            #   event.description = preferred_event["description"]
                        #   this will allow us to add the event to the calendar easier.
        previous_event = event
        count+=1
    
    return None
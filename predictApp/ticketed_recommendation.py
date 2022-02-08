"""

    Current Implementation plan:
        1. Get ticketed events from either database or the app itself
            a. I think this will happen from the app itself, getting the category preferences from the database.
        2. Get events for the next week
        3. find the last scheduled work event for the end of the day
        4. find any ticketed events that are within the categories the user likes
        5. have 2 options here, either:
            a. return the first event that fits 
            b. return all events that fit for the next week
        might fuck around and implement both aha

"""

import datetime
import calendar

#   this is the id of start_time in the calendar
START_TIME_ID = 'startTime'

# id of end_time in an event
END_TIME_ID = 'endTime'

# threshold for event recommendations
TIME_THRESHOLD = datetime.timedelta(hours=1)


def ticketed_recommendation_finder(calendar, categories):
    #   only keep events that are in the next week
    calendar = {key: value for key, value in calendar.items() if value.start_time.date() <= datetime.datetime.now().date() + datetime.timedelta(days=7)}
    
    #   sort the events by start time THIS MIGHT HAVE TO HAVE ALREADY BEEN DONE IF WE'RE ONLY GETTING THE WEEKS WORTH 
    dict(sorted(calendar.items(), key=lambda item: item[START_TIME_ID]))

    # find the last event on a given day
    previous_event = None
    for event in calendar:
        if event.id != 1: 
            #checks to see if previous_event is the last on that date.
            if event.start_time.date() != previous_event.start_time.date():
                
                return
        previous_event = event

            

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
import time
import predictApp.webscraper

#   this is the id of start_time in the calendar
START_TIME_ID = 'StartDate'

# id of end_time in an event
END_TIME_ID = 'EndDate'

# threshold for event recommendations
TIME_THRESHOLD = datetime.timedelta(hours=1)


def ticketed_recommendation_finder(calendar, categories = ""):
    #   only keep events that are in the next week
    currentDate = datetime.datetime.now().date()
    day_array = []
    event_array_by_date = [[] for i in range(7) ]
    for i in range(7):
        day_array.append(currentDate + datetime.timedelta(days=i))
    for event in calendar:
        for day in day_array:
            start_time = datetime.datetime.strptime(event[START_TIME_ID], "%Y-%m-%dT%H:%M:%SZ")
            if start_time.date() == day:
                event_array_by_date[day_array.index(day)].append(event)
    final_events = []
    for count, day in enumerate(event_array_by_date):
        final_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=count), datetime.time(hour=0, minute=0, second=0))
        for event in day:
            end_time = datetime.datetime.strptime(event[END_TIME_ID], "%Y-%m-%dT%H:%M:%SZ")
            if end_time > final_time:
                final_time = end_time
        final_events.append(final_time)
    recommended_events = []
    for end_time in final_events:
        end_of_search = datetime.datetime.combine(end_time.date()+datetime.timedelta(days=1), datetime.time(hour=4, minute=59, second=59))
        events = predictApp.webscraper.find_events(categories = categories, startDate = end_time, endDate=end_of_search)
        for event in events:
            if event["StartDate"] >= end_time + TIME_THRESHOLD:
                recommended_events.append(event)
        time.sleep(1)

    return recommended_events

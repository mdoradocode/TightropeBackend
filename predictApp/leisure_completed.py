"""
    This script finds the mindfulness events this week previous to today and the total mindfulness events this week.

"""

import datetime

def leisure_completed_calculator(events):
    #   Get only events this week
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    sat = sun + datetime.timedelta(6)

    #   get the eligible dates
    eligible_dates = []
    for event in events:
        start_date = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ').date()
        if start_date < sat and start_date > sun and event["EventType"] == 1:
            eligible_dates.append(event)
    
    #   count the number of completed events
    completed_count = 0
    for event in eligible_dates:
        event_start = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.datetime.now()
        if event_start < now:
            completed_count += 1
    
    #   number of total scheduled leisure events:
    total_count = len(eligible_dates)

    print(completed_count)
    print(total_count)
    
    return completed_count, total_count
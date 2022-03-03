"""
    This script counts the number of stressful events this week

    By: Cooper Flourens
"""

import datetime

def stress_counter(events):
    #   Get only events this week
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    sat = sun + datetime.timedelta(6)

    #   get the eligible dates
    eligible_dates = []
    for event in events:
        start_date = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ').date()
        if start_date <= sat and start_date >= sun and event["EventType"] == 0:
            eligible_dates.append(event)
    return len(eligible_dates)
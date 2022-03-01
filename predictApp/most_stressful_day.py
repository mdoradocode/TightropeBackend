"""

    This script will find the most stressful day of a given week. It will look at the current week and find which day has the longest stress event.

"""

import datetime

def most_stressful_day_calculator(events):
    # from https://stackoverflow.com/questions/18200530/get-the-last-sunday-and-saturdays-date-in-python
    #   calculates the previous sunday, aka our start date
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
    #   set up each date
    dateArray = [sun] * 7
    for i in range(len(dateArray)):
        if i == 0: continue
        dateArray[i] = dateArray[i-1] + datetime.timedelta(1)
    
    #   count the stressful events in each day
    stress_count = [0] * 7
    for i in eligible_dates:
        start_date = datetime.datetime.strptime(i["StartDate"], '%Y-%m-%dT%H:%M:%SZ').date()
        for j in range(len(dateArray)):
            start_date = datetime.datetime.strptime(i["StartDate"], '%Y-%m-%dT%H:%M:%SZ').date()
            if start_date == dateArray[j]:
                stress_count[j] += i["StressLevel"]

    #   find the day(s) with the maximum stress level
    max_days = [i for i, x in enumerate(stress_count) if x == max(stress_count)]
    stressful_days = []
    for i in max_days:
        if i == 0:
            stressful_days.append("Sunday")
        elif i == 1:
            stressful_days.append("Monday")
        elif i == 2:
            stressful_days.append("Tuesday")
        elif i == 3:
            stressful_days.append("Wednesday")
        elif i == 4:
            stressful_days.append("Thursday")
        elif i == 5:
            stressful_days.append("Friday")
        elif i == 6:
            stressful_days.append("Saturday")
        
    return stressful_days
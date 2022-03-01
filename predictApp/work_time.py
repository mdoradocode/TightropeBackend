import datetime

def work_time_calculator(events):
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
    
    #   Sum the total time of all stress events
    total_time = 0
    for event in eligible_dates:
        #   Convert start and end times into datetime objects
        start_time = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.datetime.strptime(event["EndDate"], '%Y-%m-%dT%H:%M:%SZ')
        time = end_time - start_time
        print(time.total_seconds())
        total_time += time.total_seconds()
    print("Total stress time is: " + str(total_time))
    print("Total stress time in minutes: " + str(total_time/60))
    return total_time/60/7 # minutes/day
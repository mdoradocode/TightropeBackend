"""
    An algorithmic method of forecasting stress levels
    Cooper Flourens

    Basic Outline of How this Works:
        1. Get information on all events from database
        2. Get the total work/stressful events and multiply them by the maximum stress report value
        3. Get total leisure events and multiply them by the weight, potentially based on the lenghth of time they take?
        4. Calculate stress level by:
            (sum of reported stress level of events - leisure events * weight + survey results centered around 0 * weight) / max stress level
        5. Return stress level
    
    Some current notes:
        Currently waiting on survey data to be implemented, and figure out the right weights for each category.
        We may also want to intake a "wind down" rating for different types of leisure events, and use that as sort of the reverse of the stress events.

"""

import datetime
import numpy as np

#   Define Hyperparameters
max_stress_report = 3
leisure_event_weight = 1
survey_weight =  .70
mindful_event_weight = 2
stress_event_weight = .5

def predict_stress(events, surveydata):

    #   Get events this week
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    sat = sun + datetime.timedelta(6)

    #   Categorize events
    stress_events = []
    leisure_events = []
    mindful_events = []
    for event in events:
        start_date = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ').date()
        if start_date < sat and start_date > sun and event['EventType'] == 0:
            stress_events.append(event)
        elif start_date < sat and start_date > sun and event['EventType'] == 1:
            leisure_events.append(event)
        elif start_date < sat and start_date > sun and event['EventType'] == 2:
            mindful_events.append(event)

    #   Failsafe in case there are no events this week:
    if len(stress_events) == 0:
        return 0

    # Get total number of event types
    stress_total = len(stress_events)
    leisure_total = len(leisure_events)
    mindful_total = len(mindful_events)

    # Calculate max stress level
    max_stress_level = stress_total * max_stress_report

    # Calculate current stress level
    reported_sum = 0
    for event in stress_events:
        start_date = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ')
        end_date = datetime.datetime.strptime(event["EndDate"], '%Y-%m-%dT%H:%M:%SZ')
        difference = end_date-start_date
        difference_hours = difference.total_seconds()/3600
        reported_sum += event['StressLevel'] * difference_hours
    # Calculate leisure event stress reduction
    stress_calculation = reported_sum * stress_event_weight
    leisure_calculation = leisure_total * leisure_event_weight
    survey_calculation = surveydata[0]["SurveyValue"] * survey_weight
    mindful_calculation = mindful_total * mindful_event_weight

    # Calculate real stress level
    real_stress_level = (stress_calculation - leisure_calculation - mindful_calculation + survey_calculation)

    # Create boundaries    
    if real_stress_level < 0:
        real_stress_level = 0
    if real_stress_level > 1:
        real_stress_level = 1


    print(real_stress_level)
    
    # Return stress level
    return real_stress_level
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

#   Define Hyperparameters
max_stress_report = 3
leisure_event_weight = .5
survey_weight =  1


def predict_stress(events, surveydata):

    #   Get events this week
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    sat = sun + datetime.timedelta(6)

    #   Categorize events
    stress_events = []
    leisure_events = []
    for event in events:
        print("ITERATION: ", event)
        start_date = datetime.datetime.strptime(event["StartDate"], '%Y-%m-%dT%H:%M:%SZ').date()
        if start_date < sat and start_date > sun and event['Leisure'] == False:
            print("ADDED STRESS EVENT")
            stress_events.append(event)
        elif start_date < sat and start_date > sun and event['Leisure'] == True:
            print("ADDED LEISURE EVENT")
            leisure_events.append(event)

    #   Failsafe in case there are no events this week:
    if len(stress_events) == 0:
        return 0

    # Get total number of stressful and leisure events 
    stress_total = len(stress_events)
    leisure_total = len(leisure_events)

    # Calculate max stress level
    max_stress_level = stress_total * max_stress_report

    # Calculate current stress level
    reported_sum = 0
    for event in stress_events:
        #   Stress level is not added to the event database yet, so this is going to be static
        #reported_sum += event['stress_level']
        reported_sum += 1
    # Calculate leisure event stress reduction
    leisure_calculation = leisure_total * leisure_event_weight
    # Calculate survey results
    #   PLEASE NOTE: we may need to center this data around 0 if it is a scale of 1-5 or whatever
    #   Because this is not implemented in the database yet, I'm going to set it to 0.
    #survey_calculation = sum(surveydata['values']) * survey_weight
    survey_calculation = 0

    # Calculate real stress level
    real_stress_level = (reported_sum - leisure_calculation + survey_calculation) / max_stress_level
    # Creating boundaries
    if real_stress_level > 1:
        real_stress_level = 1
    elif real_stress_level < 0:
        real_stress_level = 0
    
    # Debugging print
    print(real_stress_level)
    
    # Return stress level
    return real_stress_level
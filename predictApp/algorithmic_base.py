"""
    An algorithmic method of forecasting stress levels
    Cooper Flourens

    Current idea of how this should work:
        1. Get information on all events from database
        2. Get the total work/stressful events and multiply them by the maximum stress report value
        3. Get total leisure events and multiply them by the weight, potentially based on the lenghth of time they take?
        4. Calculate stress level by:
            (sum of reported stress level of events - leisure events * weight + survey results centered around 0 * weight) / max stress level
        5. Return stress level
    
    This is still very much in it's infancy, and I'm looking for and am open to suggestions for improvement.
    We are also waiting on testing this with the backend set up, which hopefully will be done by Tuesday, February 8, 2022.

    Some current notes:
        We may want to base this more on the survey data, because ultimately stress is a subjective thing, and a survey may give better results.
        We may also want to intake a "wound down" rating for different types of leisure events, and use that as sort of the reverse of the stress events.
        This is also still very tentative, contingent on if we get data from MIT, but it's increasingly looking like this will be the case, especially with only 2 weeks to go as of Feb 2, 2022.


"""

#   Define Hyperparameters
max_stress_report = 3
leisure_event_weight = 2
survey_weight =  1


def predict_stress(events, surveydata):

    # Currently, I believe events are passed in as a dictionary, so split it into stressful and leisure events
    stress_events = {}
    leisure_events = {}
    for event in events:
        if event['Lesiure'] == 'False':
            stress_events.append(event)
        elif event['Lesiure'] == 'True':
            leisure_events.append(event)

    # Get total number of stressful and leisure events 
    stress_total = stress_events.count()
    leisure_total = leisure_events.count()

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
import datetime
from importlib.metadata import requires
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http.response import HttpResponse
from ics import Calendar, Event
import json
import os
import pytz

from eventApp.models import Events
from eventApp.serializers import EventsSerializer

from eventApp.models import MindfulnessEvents
from eventApp.serializers import MindfulnessEventsSerializer

from eventApp.models import UserPreferences
from eventApp.serializers import UserPreferencesSerializer

from eventApp.models import StressSurvey
from eventApp.serializers import StressSurveySerializer

from eventApp.models import Streaks
from eventApp.serializers import StreaksSerializer
from eventApp.streaks import streakEvents


# Create your views here.
# At the moment this code will return all events, i will work on it later in order to make it return objects based on the UserID
@csrf_exempt
def eventsAPI(request,useremail=""):
    #Get all records that pertain to the useremail that is passed in the URL
    #Example: https://tightropeapi.herokuapp.com/events/test@test.com
    if request.method=='GET':
        #This is the same as:nevents = Events.objects.all().filter(UserEmail=useremail)
        events = Events.objects.filter(UserEmail=useremail)
        events_serializer = EventsSerializer(events, many=True)
        return JsonResponse(events_serializer.data,safe=False)

    #Add a record, must include all data EXCEPT for the the EventID, which is auto generated by the model
    #Example: https://tightropeapi.herokuapp.com/events/
    elif request.method=='POST':
        events_data = JSONParser().parse(request)
        events_serializer = EventsSerializer(data=events_data)
        events_serializer.is_valid()
        print(events_serializer.errors)
        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Added event!", safe=False)
        return JsonResponse("Failed to add event.", safe=False)

    #Update a record by passing a full JSON request, that includes all information for the event INCLUDING the EventID within the request
    #Example: https://tightropeapi.herokuapp.com/events/
    elif request.method=='PUT':
        events_data = JSONParser().parse(request)
        events=Events.objects.get(EventID=events_data['EventID'])
        events_serializer = EventsSerializer(events,data=events_data)
        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Updated event!",safe=False)
        return JsonResponse("Failed to update event.", safe=False)
    
    #Find and delete a record by passing a full JSON request, that includes all information for the event INCLUDING the EventID within the request
    #Example: https://tightropeapi.herokuapp.com/events/
    elif request.method=='DELETE':
        events=Events.objects.get(EventID=useremail)
        events.delete()
        return JsonResponse("Deleted Sucessfully!",safe=False)
    


@csrf_exempt
def mindfulnesseventsAPI(request):
    #Get the record that pertains to the minfulness event name
    #Example: 
    if request.method=='GET':
        mindfulness_events = MindfulnessEvents.objects.all()
        serialized_mindfulness_events = MindfulnessEventsSerializer(mindfulness_events, many=True)
        return JsonResponse(serialized_mindfulness_events.data,safe=False)

    #Add a record, must include all data EXCEPT for the the MindfulnessEventID, which is auto generated by the model
    #Example: 
    elif request.method=='POST':
        new_data = JSONParser().parse(request)
        serialized_mindfulness_events = MindfulnessEventsSerializer(data=new_data)
        serialized_mindfulness_events.is_valid()
        print(serialized_mindfulness_events.errors)
        if serialized_mindfulness_events.is_valid():
            serialized_mindfulness_events.save()
            return JsonResponse("Added new Mindfulness Event!", safe=False)
        return JsonResponse("Failed to add event.", safe=False)

    #Update a record by passing a full JSON request, that includes all information for the event INCLUDING the MindfulnessEventID within the request
    #Example: 
    elif request.method=='PUT':
        events_data = JSONParser().parse(request)
        events=MindfulnessEvents.objects.get(MindfulnessEventID=events_data['MindfulnessEventID'])
        events_serializer = MindfulnessEventsSerializer(events,data=events_data)
        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Updated event!",safe=False)
        return JsonResponse("Failed to update event.", safe=False)
    
    #Find and delete a record by passing a full JSON request, that includes all information for the event INCLUDING the MindfulnessEventID within the request
    #Example: 
    elif request.method=='DELETE':
        events_data = JSONParser().parse(request)
        event=MindfulnessEvents.objects.get(MindfulnessEventID=events_data['MindfulnessEventID'])
        event.delete()
        return JsonResponse("Deleted Sucessfully!",safe=False)
  


@csrf_exempt
def userMindfulnessPreferences(request, useremail=""):
    #Get a given user's mindfulness preferences
    if request.method=='GET':
        userpreferences = UserPreferences.objects.filter(UserEmail=useremail)
        serialized_preferences = UserPreferencesSerializer(userpreferences, many=True)
        return JsonResponse(serialized_preferences.data,safe=False)

    #Takes a single request for a user's preferences and adds it to database
    if request.method=='POST':
        user_preferences = JSONParser().parse(request)
        list = user_preferences['mindfulPreferenceIDs']
        for i in list:
            query_base_event=MindfulnessEvents.objects.filter(MindfulnessEventID=i)
            user_preference_dictionary = {}
            for base_event in query_base_event:
                user_preference_dictionary = {
                    'UserEmail': useremail,
                    'UserPreference': base_event.MindfulnessEventName,
                    'UserPreferenceDuration': base_event.MindfulnessEventDuration,
                    'UserPreferenceNotes': base_event.MindfulnessEventNotes
                }
            serialized_preferences = UserPreferencesSerializer(data=user_preference_dictionary)
            serialized_preferences.is_valid()
            print(serialized_preferences.errors)
            if serialized_preferences.is_valid():
                serialized_preferences.save()
            else:
                return JsonResponse("Failed to add event", safe=False)
        return JsonResponse("Successfully Added Preferences", safe=False)

    #I don't think this is relevant, this could be used to update a record of the user's preferences, but its standard
    if request.method=='PUT':
        print("CHECK")
        for event in UserPreferences.objects.filter(UserEmail=useremail):
            print(event)
            event.delete()
        print("DELETED!")
        user_preferences = JSONParser().parse(request)
        list = user_preferences['mindfulPreferenceIDs']
        print("CHECK2")
        for i in list:
            query_base_event=MindfulnessEvents.objects.filter(MindfulnessEventID=i)
            user_preference_dictionary = {}
            for base_event in query_base_event:
                user_preference_dictionary = {
                    'UserEmail': useremail,
                    'UserPreference': base_event.MindfulnessEventName,
                    'UserPreferenceDuration': base_event.MindfulnessEventDuration,
                    'UserPreferenceNotes': base_event.MindfulnessEventNotes
                }
            serialized_preferences = UserPreferencesSerializer(data=user_preference_dictionary)
            serialized_preferences.is_valid()
            print(serialized_preferences.errors)
            if serialized_preferences.is_valid():
                serialized_preferences.save()
            else:
                return JsonResponse("Failed to add event", safe=False)
        return JsonResponse("Successfully Added Preferences", safe=False)

    #Deletes a record of a user's preferences
    #To me, this looks like it wouldn't work, might have to reqork this later
    if request.method=='DELETE':
        deletion = JSONParser().parse(request)
        event=UserPreferences.objects.get(UserPreferenceID=deletion['UserPreferenceID'])
        event.delete()
        return JsonResponse("Deleted Sucessfully!",safe=False)


@csrf_exempt
def surveyApp(request, useremail=""):
    if request.method=='GET':
        result = StressSurvey.objects.filter(UserEmail=useremail)
        serialized_survey = StressSurveySerializer(result, many=True)
        return JsonResponse(serialized_survey.data,safe=False)
    
    if request.method=='POST':
        survey_results = JSONParser().parse(request)
        serialized_survey_results = StressSurveySerializer(data=survey_results)
        serialized_survey_results.is_valid()
        print(serialized_survey_results.errors)
        if serialized_survey_results.is_valid():
            serialized_survey_results.save()
            return JsonResponse("Added new Stress Survey Result!", safe=False)
        return JsonResponse("Failed to add new result.", safe=False)
    
    if request.method=='PUT':
        new_value = JSONParser().parse(request)
        old_value=StressSurvey.objects.get(UserEmail=useremail)
        events_serializer = StressSurveySerializer(old_value, data=new_value)
        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Updated stress value!",safe=False)
        return JsonResponse("Failed to update stress value.", safe=False)
    
    if request.method=='DELETE':
        events=StressSurvey.objects.filter(UserEmail=useremail)
        for event in events:
            event.delete()
        return JsonResponse("Deleted Sucessfully!",safe=False)


#This one is wonky GET will return a list of events AND the user data pertaining to streaks in a single JSON response through a list
@csrf_exempt
def streaks(request,useremail=""):

    #Returns a list of eligible events (within a time frame) and the user data for said events
    if request.method == 'GET':
        #Next three lines are for debugging what records are in the database, can be commented out and gotten rid of as needed
        allUserData = Streaks.objects.all()
        allUserData_serializer = StreaksSerializer(allUserData,many=True)
        #print("All Users in DB: ", allUserData_serializer.data)
        
        #Grab and serialize all the data for the user
        user_streaks = Streaks.objects.filter(UserEmail = useremail)
        user_streaks_serializer = StreaksSerializer(user_streaks,many=True)

        #Use the user data and the streakEvents method to determine which event objects should go on the list
        event_list = streakEvents(user_streaks_serializer.data[0])

        #Make a list object out of the two above list objects
        jsonReturnList = [user_streaks_serializer.data, event_list]

        #return the list of lists
        return JsonResponse(jsonReturnList, safe=False)

    #Method only to be user wil NEW users
    elif request.method=='POST':
        #Define a new initial user from the email passed in the routing
        streaks_data = {
                        "UserEmail": useremail,
                        "StreakCount": 0,
                        "LastLogin": datetime.datetime.now().replace(microsecond=0)
        }
        #Serialize the and save the data
        streaks_serializer = StreaksSerializer(data=streaks_data)
        streaks_serializer.is_valid()
        #print(streaks_serializer.errors)
        if streaks_serializer.is_valid():
            streaks_serializer.save()
            return JsonResponse("Added User!", safe=False)
        return JsonResponse("Failed to add User.", safe=False)

    #Update a user profile that already exists
    elif request.method == 'PUT':
        #Parse up the data in the request
        streaks = JSONParser().parse(request)
        #Get the user record that pertains to the email in the body
        streaks_user_data = Streaks.objects.get(UserEmail = streaks['UserEmail'])
        #replace the old data (streaks_user_data) with the new data (streaks)
        streaks_serializer = StreaksSerializer(streaks_user_data, data=streaks)
        if(streaks_serializer.is_valid()):
            streaks_serializer.save()
            return JsonResponse("Streaks object successfully updated!", safe=False)
        return JsonResponse("Unable to update streaks object!", safe=False)

    #Delete a record based on the UserID that will be passed in the place of useremail
    elif request.method=='DELETE':
        streaks_data=Streaks.objects.get(UserID=useremail) #Useremail = UserID in this call
        #data.delete()
        #print(streaks_data.StreakCount)
        #print(streaks_data.LifetimeScheduledMindful)
        streaks_data.StreakCount = 0
        streaks_data.LifetimeScheduledMindful = 0
        #print(streaks_data.StreakCount)
        #print(streaks_data.LifetimeScheduledMindful)
        streaks_data.save()
        return JsonResponse("Reset Streaks Sucessfully!",safe=False)

@csrf_exempt
def ics(request, useremail=""):
    if request.method=='GET':
        events = Events.objects.filter(UserEmail=useremail)
        events_serializer = EventsSerializer(events, many=True)
        calendar = Calendar()
        for event in events_serializer.data:
            e = Event()
            e.name = event["EventName"]
            tz = pytz.timezone("US/Pacific")
            e.begin = tz.localize(datetime.datetime.strptime(event["StartDate"], "%Y-%m-%dT%H:%M:%SZ"), is_dst=None)
            e.end = tz.localize(datetime.datetime.strptime(event["EndDate"], "%Y-%m-%dT%H:%M:%SZ"), is_dst=None)
            e.description = event["Notes"]
            e.location = event["Location"]
            calendar.events.add(e)
            calendar.events
        
        filename = useremail + "_calendar.ics"
        filepath = "static/ics/" + filename
        if os.path.exists(filepath):
            os.remove(filepath)
        f = open(filepath, 'w')
        f.write(str(calendar))
        f.close()
        file = "/static/ics/"
        fl = open(filepath, 'r')
        response = HttpResponse(fl, content_type=ics)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    
    if request.method=='POST':
        data = request.FILES['calendar']
        string = ""
        for line in data:
            string += line.decode('UTF-8')
        c = Calendar(string)
        tz = pytz.timezone("US/Pacific")
        for e in c.events:
            start_time = e.begin.astimezone(tz)
            end_time = e.end.astimezone(tz)
            event = {
                "UserEmail": useremail,
                "EventName": e.name,
                "StartDate": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "EndDate": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "Location": e.location,
                "EventType": 4,
                "StressLevel": 0,
                "Notes": e.description
            }
            events_serializer = EventsSerializer(data=event)
            events_serializer.is_valid()
        
            if events_serializer.is_valid():
                events_serializer.save()
            else:
                return JsonResponse("Operation Failed. Please Try Again.", safe=False)

        return JsonResponse("Added Calendar!", safe=False)
    
    if request.method == 'PUT':
        events_data = JSONParser().parse(request)
        event=Events.objects.filter(EventID=events_data['EventID'])
        event_serialized = EventsSerializer(event, many=True)
        calendar = Calendar()
        for event in event_serialized.data:
            print(event)
            e = Event()
            e.name = event["EventName"]
            tz = pytz.timezone("US/Pacific")
            e.begin = tz.localize(datetime.datetime.strptime(event["StartDate"], "%Y-%m-%dT%H:%M:%SZ"), is_dst=None)
            e.end = tz.localize(datetime.datetime.strptime(event["EndDate"], "%Y-%m-%dT%H:%M:%SZ"), is_dst=None)
            e.description = event["Notes"]
            e.location = event["Location"]
            calendar.events.add(e)
            calendar.events
        filename = event["EventName"].replace(" ", "") + ".ics"
        filepath = "static/ics/" + filename
        if os.path.exists(filepath):
            os.remove(filepath)
        f = open(filepath, 'w')
        f.write(str(calendar))
        f.close()
        file = "/static/ics/"
        fl = open(filepath, 'r')
        response = HttpResponse(fl, content_type=ics)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
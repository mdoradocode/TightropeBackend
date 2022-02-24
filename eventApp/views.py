from importlib.metadata import requires
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from eventApp.models import Events
from eventApp.serializers import EventsSerializer

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
        events_data = JSONParser().parse(request)
        events=Events.objects.get(EventID=events_data['EventID'])
        events.delete()
        return JsonResponse("Deleted Sucessfully!",safe=False)
    
@csrf_exempt
def mindfulnesseventsAPI(request):
    #Get the record that pertains to the minfulness event name
    #Example: 
    if request.method=='GET':
        pass

    #Add a record, must include all data EXCEPT for the the MindfulnessEventID, which is auto generated by the model
    #Example: 
    elif request.method=='POST':
        pass

    #Update a record by passing a full JSON request, that includes all information for the event INCLUDING the MindfulnessEventID within the request
    #Example: 
    elif request.method=='PUT':
        pass
    
    #Find and delete a record by passing a full JSON request, that includes all information for the event INCLUDING the MindfulnessEventID within the request
    #Example: 
    elif request.method=='DELETE':
        pass
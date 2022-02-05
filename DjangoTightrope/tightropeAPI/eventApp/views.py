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
def eventsAPI(request,id=0):
    #Get all records (temp)
    if request.method=='GET':
        events = Events.objects.all()
        events_serializer = EventsSerializer(events, many=True)
        return JsonResponse(events_serializer.data,safe=False)

    #Add a record
    elif request.method=='POST':
        events_data = JSONParser().parse(request)
        events_serializer = EventsSerializer(data=events_data)
        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Added event!", safe=False)
        return JsonResponse("Failed to add event.", safe=False)

    #update a record
    elif request.method=='PUT':
        events_data = JSONParser().parse(request)
        events=Events.objects.get(EventID=events_data['EventID'])
        events_serializer = EventsSerializer(events,data=events_data)
        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Updated event!",safe=False)
        return JsonResponse("Failed to update event.", safe=False)
    
    elif request.method=='DELETE':
        events=Events.objects.get(EventID=id)
        events.delete()
        return JsonResponse("Deleted Sucessfully!",safe=False)
    
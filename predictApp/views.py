#   Base Library Imports
from importlib.metadata import requires
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from predictApp.algorithmic_base import predict_stress

from eventApp.models import Events
from eventApp.serializers import EventsSerializer



# Create your views here.
@csrf_exempt
def predictAPI(request,id=0):
    #   Gets the stress prediction based on current events
    if request.method=='GET':
        events = Events.objects.all()
        events_serializer = EventsSerializer(events, many=True)
        stress_value = predict_stress(events_serializer.data, surveydata = 0)
        #   I don't know if this is going to work. I might have to make a stress-prediction class and return that, but we will try.
        return JsonResponse(str(stress_value), safe=False)

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
    

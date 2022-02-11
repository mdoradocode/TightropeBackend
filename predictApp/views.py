#   Base Library Imports
from importlib.metadata import requires
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from predictApp.algorithmic_base import predict_stress
from predictApp.most_stressful_day import most_stressful_day_calculator
from predictApp.work_time import work_time_calculator
from predictApp.leisure_completed import leisure_completed_calculator
from predictApp.stress_counter import stress_counter

from eventApp.models import Events
from eventApp.serializers import EventsSerializer



# Create your views here.
@csrf_exempt
def predictAPI(request,useremail=""):
    #   Gets the stress prediction based on current events
    if request.method=='GET':
        events = Events.objects.filter(UserEmail=useremail)
        events_serializer = EventsSerializer(events, many=True)
        stress_value = predict_stress(events_serializer.data, surveydata = 0)
        #   I don't know if this is going to work. I might have to make a stress-prediction class and return that, but we will try.
        return JsonResponse(str(stress_value), safe=False)
    
@csrf_exempt
def stressful_day(request, useremail=""):
    #   Gets the most stressful day based on this week's events
    if request.method=="GET":
        events = Events.objects.filter(UserEmail=useremail)
        events_serializer = EventsSerializer(events, many=True)
        stress_days = most_stressful_day_calculator(events_serializer.data)
        return JsonResponse(stress_days, safe=False)

@csrf_exempt
def worktime(request, useremail=""):
    #   Gets the average daily work time based on this week's events
    if request.method=="GET":
        events = Events.objects.filter(UserEmail=useremail)
        events_serializer = EventsSerializer(events, many=True)
        work_time = work_time_calculator(events_serializer.data)
        return JsonResponse(work_time, safe=False)

@csrf_exempt
def leisure_calculator(request, useremail=""):
    #   gets number of completed and scheduled leisure events
    if request.method=="GET":
        events = Events.objects.filter(UserEmail=useremail)
        events_serializer = EventsSerializer(events, many=True)
        leisure_completed = leisure_completed_calculator(events_serializer.data)
        #ratio = leisure_completed[0]/leisure_completed[1]
        return JsonResponse(leisure_completed, safe=False)

@csrf_exempt
def stress_counter_view(request, useremail=""):
    #   Counts stressful events this week
    if request.method=="GET":
        events = Events.objects.filter(UserEmail=useremail)
        events_serializer = EventsSerializer(events, many=True)
        stress_count = stress_counter(events_serializer.data)
        return JsonResponse(stress_count, safe=False)
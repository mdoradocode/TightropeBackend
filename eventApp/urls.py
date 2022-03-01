from django.urls import path

from eventApp import views

urlpatterns=[
    #Route requests with the event tag on them to the events api
    path(r'events/',views.eventsAPI),
    #if the request has an UserEmail attached (it will) also route it to the API
    path(r'events/<str:useremail>',views.eventsAPI),

    #Route requests with the event tag on them to the events api
    path(r'mindfulnessevents/',views.mindfulnesseventsAPI),
    #if the request has an UserEmail attached (it will) also route it to the API
    path(r'mindfulnessevents/<str:useremail>',views.mindfulnesseventsAPI),

    #User Preference Manipulation
    path(r'mindfulpreference/<str:useremail>',views.userMindfulnessPreferences),
    path(r'mindfulpreference/<str:useremail>',views.userMindfulnessPreferences),

    #Stress Survey
    path(r'stresssurvey/<str:useremail>',views.surveyApp)
]
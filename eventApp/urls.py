from django.urls import path

from eventApp import views

urlpatterns=[
    #Route requests with the event tag on them to the events api
    path(r'events/',views.eventsAPI),
    #if the request has an UserEmail attached (it will) also route it to the API
    path(r'events/<str:useremail>',views.eventsAPI)
]
from django.urls import path

from predictApp import views

urlpatterns=[
    #This gets the user's stress level prediction
    path(r'predict/',views.predictAPI),
    #if the request has an id attached (it will) also route it to the API
    path(r'predict/<int:id>',views.predictAPI),
    #returns the most stressful day
    path(r'stressday/',views.stressful_day)
]
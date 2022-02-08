from django.urls import path

from predictApp import views

urlpatterns=[
    #Route requests with the event tag on them to the events api
    path(r'predict/',views.predictAPI),
    #if the request has an id attached (it will) also route it to the API
    path(r'predict/<int:id>',views.predictAPI)

]
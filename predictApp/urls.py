from django.urls import path

from predictApp import views

urlpatterns=[
    #This gets the overall stress level prediction. Not useful, but interesting :)
    path(r'predict/',views.predictAPI),
    #if the request has an id attached (it will) also route it to the API
    path(r'predict/<str:useremail>',views.predictAPI),
    #returns the most stressful day
    path(r'stressday/<str:useremail>',views.stressful_day),
    #returns the work time
    path(r'worktime/<str:useremail>',views.worktime),
    #returns completed leisures, total leisures
    path(r'leisurecalculator/<str:useremail>',views.leisure_calculator),
    #returns the stress count
    path(r'stresscounter/<str:useremail>',views.stress_counter_view),
    #returns the ticketed recommendation
    path(r'localevents/<str:useremail>',views.local_event_recommendations),
    #returns a mindfulness recommendation
    path(r'mindfulnessrecommender/<str:useremail>',views.mindfulness_event_recommendations)
]
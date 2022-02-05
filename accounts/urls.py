from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from accounts import views

urlpatterns = [
    #Profile view is for the backend development
    path('profile/',views.ProfileView.as_view()),
    #This accesses the CustomAuthToken function in the views for accounts
    path('api/auth/', views.CustomAuthToken.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
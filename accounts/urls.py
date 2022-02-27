from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from accounts import views

urlpatterns = [
    #Profile view is for authenticated user actions (NOT POST)
    path('profile/',views.ProfileView.as_view()),
    #This path is for adding users, it cannot be in the "profile" class because new users have no authentication
    #Anyone can add a user here
    path('profileAdd/', views.ProfileAdd.as_view()),
    #This accesses the CustomAuthToken function in the views for accounts
    path('api/auth/', views.CustomAuthToken.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

#This is a dev thing to see the admin info of Django
class IndexView(APIView):
    def get(self, request, format=None):
        content = {"You are accessing the tightrope user authentication API, congrats!"}
        
        return Response(content)

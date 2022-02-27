from json import JSONDecodeError
from logging import raiseExceptions
from multiprocessing import context
from multiprocessing.sharedctypes import Value
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from accounts.serializer import UserSerializer

#View all profiles registered in the Django Database
class ProfileView(APIView):
    #There are three ways to authenticate a request. A session ID, Basic authentication (Username and password),
    #or Token Authentication. We use Basic and Token here, it needs to be passed as a header option in the request
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
         #This returns the requested user based off of the front end's current user's token
    def get(self, request, format=None):
        #Fill the content of the response with information from the user database and retiurn that response
        content = {
            'user email': str(request.user.email),  # `django.contrib.auth.User` instance.
            'user': str(request.user), #Is really just the username
            'userFirstName': str(request.user.first_name),
            'userLastName': str(request.user.last_name),
            'password': str(request.user.password), #Returns a hashed password
            'auth': str(request.auth),  # Token associated with the user
        }
        return Response(content) #Actual response that is send back, not sure how secure this is
    
    #This method will change an aspect of a users profile
    def put(self,request, format=None):
        #Parse the request that holds one key value pait
        user_data = JSONParser().parse(request)
        #Grab the users token from the Authorization field in the http header
        token = request.auth
        #Turn the key/value into lists so we may access the fields seperately 
        user_key = list(user_data.keys())[0]
        user_value = list(user_data.values())[0]
        #Find the user we are working with based on their token
        user = User.objects.get(auth_token=token)
        #Change a required field based on which request was made
        if(user_key == 'username'):
            user.username = user_value
            user.save()
            return JsonResponse("Username Sucessfully Updated!", safe=False)
        if(user_key == 'first_name'):
            user.first_name = user_value
            user.save()
            return JsonResponse("First Name Sucessfully Updated!", safe=False)
        if(user_key == 'last_name'):
            user.last_name = user_value
            user.save()
            return JsonResponse("Last Name Sucessfully Updated!", safe=False)
        if(user_key == 'email'):
            user.email = user_value
            user.username = user_value
            user.save()
            return JsonResponse("Email Sucessfully Updated!", safe=False)
        if(user_key == 'password'):
            #Hash the password before storage
            user.password = make_password(user_value)
            user.save()
            return JsonResponse("Password Sucessfully Updated!", safe=False)
        return JsonResponse("Unable To Update Field!", safe=False)

    #This method will delete a user from the database based on their token
    def delete(self, request, format=None):
        #Grab the token from the Authorization key/value pair in the header
        token = request.auth
        #Find the user based on that token
        user = User.objects.get(auth_token=token)
        #If the delete is sucessful or fails return the correct error message
        if(user.delete()):
            return JsonResponse("User Successfully Deleted!", safe=False)
        return JsonResponse("Unable To Delete User", safe=False)

        



class ProfileAdd(APIView):
    #This function will take in a user object consisting of the following fields and save the user to the database
    #Fields required (in order) username, first_name, last_name, email, password
    #Note: If a user with the username already exists, it cannot add the user to the data base
    def post(self, request, format=None):
        #Take in the user request data and parse
        user_data = JSONParser().parse(request)
        #Serialize it to make sure all fields are present and in the correct format (dict)
        user_serializer = UserSerializer(data=user_data)
        #Validate Data
        if user_serializer.is_valid():
            #Create a user object with the passed username, email, and password
            #Hasing is handled by the function
            user = User.objects.create_user(user_data['username'],user_data['email'],user_data['password'])
            #Add the Users last_name
            user.last_name = user_data['last_name']
            #Add the Users first_name
            user.first_name = user_data['first_name']
            #Save the user
            user.save()
            #Respond to the request, confirming success
            return JsonResponse("User Sucessfully Added!",safe=False)
        #If an error occurs becuase the data doesnt serialize or any other reason (duplicate user)
        elif(user_serializer.errors):
            #Grab the error
            error = user_serializer.errors
            #Extract the name of the error
            errorName = list(error.keys())[0]
            #Extract the detail of the error
            errorDetail = list(error.values())[0][0]
            #Return a custom error response
            return JsonResponse("Unable To Add User Because -> " + errorName + ': ' + errorDetail,safe=False)
        #General failure to add response for edge cases
        return JsonResponse("Unable To Add User",safe=False)



#Put the user information into the django database and return the record for it
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'userFirstName': user.first_name,
            'userLastName': user.last_name
        })
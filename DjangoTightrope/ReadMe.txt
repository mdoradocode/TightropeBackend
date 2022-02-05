FOR SIMPLICITY: I'm adding a list of what to do to set django up on your local machine.

macOS:
    1. Ensure python is installed:
        python --version
        a. this should be version 3.9 or greater. If it shows as 2.x, you may have python3 installed. Simply do:
            python3 --version
        if this is the case, you can either change it using another guide or you can do all python commands using python3 instead of python.
    2. Navigate to the DjangoTightrope folder and activate the virtual environment:
        source venv/bin/activate
    3. Navigate to the tightropeAPI folder and install the requirements using pip:
        pip install -r requirements.txt
    4. Start the Django project using:
        python manage.py runserver

This should get the server up and running. If you need more specific help, contact Cooper or Michael.




The following documentation describes how Michael built the Django end from scratch. 
This process is not nessecary for every team member, but if you are having issues
with compatability or virtual env, this documentation may be useful:

    Install python to macOS:
        brew install python3

    Change the default python to python 3.9:
        ln -s -f /usr/local/bin/python3.9 /usr/local/bin/python

    Check which version is default (should be python 3.9):
        python --version

    Navigate to the tightropeDjango folder and create a virtual environment:
        python -m venv venv

    Activate the virtual environmentto work in:
        source venv/bin/activate

    Install Django to the virtual environment (not your local directory):
        pip install django

    Install  Django REST Framework, which is a library needed for Database communication and API stuff:
        pip install djangorestframework
    
    Create the Django project:
        django-admin startproject tightropeAPI
    
    Install CORS, which is a service that allows different domains to access the API (this will allows
    Angular to access the Django API {very cool}):
        pip install django-cors-headers
    
    Now you go to settings.py and add "corsheaders" to "INSTALLED_APPS" and "corsheaders.middleware.CorsMiddleware" to "MIDDLEWARE"

    Now between "INSTALLED_APPS" and "MIDDLEWARE", we need to tell CORS to allow some websites.
        I will be putting "CORS_ORIGIN_ALLOW_ALL = True" which will white list all domains. 
        
        In the future we may want to change this for security reasons. We can whitelist specific sites using this:
            CORS_ORIGIN_WHITELIST = ('http://websitename.com')

    So now we are going to make an app within the project, we may make mutiple apps to do different things, right now I will make an app that returns events.

    To create an app:
        python manage.py startapp eventApp

    Within the first folder named "tightropeAPI" (the project folder that contains an app folder named "tightropeAPI") create an event app:
        python manage.py startapp eventApp
    
    Then register INSTALLED_APPS in the settings.py file
        eventApp.apps.EventappConfig

    Then register the rest framework in INSTALLED_APPS  in settings.py:
        rest_framework

    At this point I went to the eventApp models.py folder and added the class Events.

    I then perform a migration to tell the db that we should have this table, all from the top level tightropeAPI folder:
        python manage.py makemigrations eventApp
    
    And then actually perform the migration:
        python manage.py migrate

    Now we have made a table called Events within the Database.

    We will now create Serializers in order to turn our 
    classes into native python types. Within the eventApp, make a file called serializers.py. Within it we define what makes up an Events class.

    Now we create the views withihn eventApp. csrf_exempt allows for access.

    Then we route the API methods by creating a new urls.py file within eventApp. Include these new urls in the main url file of the tightropeAPI.
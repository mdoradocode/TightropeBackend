from django.db import models

# Create your models here.

class Events(models.Model):
    EventID = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=50)
    EventName = models.CharField(max_length=100)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    Location = models.CharField(max_length=50)
    EventType = models.IntegerField()
    StressLevel = models.IntegerField()
    Notes = models.CharField(max_length=500)
    
class MindfulnessEvents(models.Model):
    MindfulnessEventID = models.AutoField(primary_key=True)
    MindfulnessEventName = models.CharField(max_length=100)
    MindfulnessEventDuration = models.IntegerField()
    MindfulnessEventNotes = models.CharField(max_length=500)

class UserPreferences(models.Model):
    UserPreferenceID = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=50)
    UserPreference = models.CharField(max_length=100)
    UserPreferenceDuration = models.IntegerField()
    UserPreferenceNotes = models.CharField(max_length=500)

class StressSurvey(models.Model):
    SurveyID = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=50)
    SurveyValue = models.IntegerField()
from django.db import models

# Create your models here.

class Events(models.Model):
    EventID = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=25)
    EventName = models.CharField(max_length=25)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    Location = models.CharField(max_length=25)
    EventType = models.IntegerField()
    StressLevel = models.IntegerField()
    Notes = models.CharField(max_length=100)
    
class MindfulnessEvents(models.Model):
    MindfulnessEventID = models.AutoField(primary_key=True)
    MindfulnessEventName = models.CharField(max_length=50)
    MindfulnessEventDuration = models.IntegerField()
    MindfulnessEventNotes = models.CharField(max_length=300)

class userPrefMindEvents(models.Model):
    userMindEventID = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=25)
    eventpref = models.CharField(max_length=50)
    
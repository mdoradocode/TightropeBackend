from django.db import models

# Create your models here.

class Events(models.Model):
    EventID = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=25)
    EventName = models.CharField(max_length=25)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    Location = models.CharField(max_length=25)
    Leisure = models.BooleanField()
    StressLevel = models.IntegerField()
    Notes = models.CharField(max_length=100)
    

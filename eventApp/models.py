from django.db import models

# Create your models here.

class Events(models.Model):
    EventID = models.AutoField(primary_key=True)
    UserID = models.CharField(max_length=25)
    EventName = models.CharField(max_length=50)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    Description = models.CharField(max_length=100)
    Lesiure = models.BooleanField()
